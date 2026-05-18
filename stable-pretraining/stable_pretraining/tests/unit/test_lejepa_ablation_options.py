import pytest
import torch

from stable_pretraining.methods.lejepa import LeJEPA


def _assert_training_forward(model):
    model.train()
    global_views = [
        torch.randn(2, 3, 224, 224),
        torch.randn(2, 3, 224, 224),
    ]
    local_views = [
        torch.randn(2, 3, 96, 96),
        torch.randn(2, 3, 96, 96),
    ]

    output = model(global_views=global_views, local_views=local_views)

    assert output.loss.shape == ()
    assert torch.isfinite(output.loss)
    assert torch.isfinite(output.inv_loss)
    assert torch.isfinite(output.sigreg_loss)
    assert output.embedding.shape == (4, model.embed_dim)
    return output


@pytest.mark.parametrize("projector_arch", ["Linear", "MLP2", "MLP", "MLP4"])
def test_lejepa_projector_arch_forward(projector_arch):
    torch.manual_seed(0)
    model = LeJEPA(
        encoder_name="vit_tiny_patch16_224",
        n_slices=8,
        n_points=5,
        pretrained=False,
        drop_path_rate=0.0,
        projector_arch=projector_arch,
    )
    _assert_training_forward(model)


@pytest.mark.parametrize("sigreg_target", ["proj", "embed", "both"])
def test_lejepa_sigreg_target_forward(sigreg_target):
    torch.manual_seed(0)
    model = LeJEPA(
        encoder_name="vit_tiny_patch16_224",
        n_slices=8,
        n_points=5,
        pretrained=False,
        drop_path_rate=0.0,
        sigreg_target=sigreg_target,
    )
    _assert_training_forward(model)


def test_lejepa_invalid_sigreg_target_raises():
    with pytest.raises(ValueError, match="sigreg_target"):
        LeJEPA(
            encoder_name="vit_tiny_patch16_224",
            n_slices=8,
            n_points=5,
            pretrained=False,
            sigreg_target="invalid",
        )


@pytest.mark.parametrize("predictor", ["none", "linear", "mlp"])
def test_lejepa_predictor_forward(predictor):
    torch.manual_seed(0)
    model = LeJEPA(
        encoder_name="vit_tiny_patch16_224",
        n_slices=8,
        n_points=5,
        pretrained=False,
        drop_path_rate=0.0,
        predictor=predictor,
    )
    _assert_training_forward(model)


def test_lejepa_invalid_predictor_raises():
    with pytest.raises(ValueError, match="predictor"):
        LeJEPA(
            encoder_name="vit_tiny_patch16_224",
            n_slices=8,
            n_points=5,
            pretrained=False,
            predictor="invalid",
        )


def test_lejepa_reg_tokens_zero_forward():
    torch.manual_seed(0)
    model = LeJEPA(
        encoder_name="vit_tiny_patch16_224",
        n_slices=8,
        n_points=5,
        pretrained=False,
        drop_path_rate=0.0,
        reg_tokens=0,
    )

    assert model.reg_tokens == 0
    assert getattr(model.backbone, "num_reg_tokens", 0) == 0
    _assert_training_forward(model)


@pytest.mark.parametrize("reg_tokens", [1, 2])
def test_lejepa_reg_tokens_forward_when_timm_supports(reg_tokens):
    torch.manual_seed(0)
    try:
        model = LeJEPA(
            encoder_name="vit_tiny_patch16_224",
            n_slices=8,
            n_points=5,
            pretrained=False,
            drop_path_rate=0.0,
            reg_tokens=reg_tokens,
        )
    except ValueError as exc:
        if "reg_tokens" in str(exc):
            pytest.skip(f"timm does not support reg_tokens here: {exc}")
        raise

    assert model.reg_tokens == reg_tokens
    assert model.backbone.num_reg_tokens == reg_tokens
    _assert_training_forward(model)


def test_lejepa_reg_tokens_unsupported_backbone_error_message():
    with pytest.raises(ValueError, match="does not support reg_tokens=1"):
        LeJEPA(
            encoder_name="resnet18",
            n_slices=8,
            n_points=5,
            pretrained=False,
            reg_tokens=1,
        )


@pytest.mark.parametrize(
    ("aggregator", "dim_multiplier"),
    [("cls", 1), ("mean", 1), ("cls_mean", 2)],
)
def test_lejepa_aggregator_forward_and_dimensions(aggregator, dim_multiplier):
    torch.manual_seed(0)
    model = LeJEPA(
        encoder_name="vit_tiny_patch16_224",
        n_slices=8,
        n_points=5,
        pretrained=False,
        drop_path_rate=0.0,
        aggregator=aggregator,
    )

    assert model.aggregator == aggregator
    assert model.embed_dim == model.backbone_embed_dim * dim_multiplier

    projected = model.projector(torch.randn(2, model.embed_dim))
    assert projected.shape == (2, 512)
    _assert_training_forward(model)


def test_lejepa_aggregator_mean_ignores_cls_and_register_tokens():
    model = LeJEPA(
        encoder_name="vit_tiny_patch16_224",
        n_slices=8,
        n_points=5,
        pretrained=False,
        drop_path_rate=0.0,
        reg_tokens=2,
        aggregator="mean",
    )
    tokens = torch.tensor(
        [[[100.0, 100.0], [200.0, 200.0], [300.0, 300.0], [1.0, 3.0], [5.0, 7.0]]]
    )

    aggregated = model.aggregate_tokens(tokens)

    assert torch.equal(aggregated, torch.tensor([[3.0, 5.0]]))


def test_lejepa_aggregator_cls_mean_concatenates_cls_and_patch_mean():
    model = LeJEPA(
        encoder_name="vit_tiny_patch16_224",
        n_slices=8,
        n_points=5,
        pretrained=False,
        drop_path_rate=0.0,
        reg_tokens=1,
        aggregator="cls_mean",
    )
    tokens = torch.tensor(
        [[[10.0, 20.0], [100.0, 100.0], [1.0, 3.0], [5.0, 7.0]]]
    )

    aggregated = model.aggregate_tokens(tokens)

    assert torch.equal(aggregated, torch.tensor([[10.0, 20.0, 3.0, 5.0]]))


def test_lejepa_invalid_aggregator_raises():
    with pytest.raises(ValueError, match="aggregator"):
        LeJEPA(
            encoder_name="vit_tiny_patch16_224",
            n_slices=8,
            n_points=5,
            pretrained=False,
            aggregator="cls2",
        )


@pytest.mark.parametrize("patch_mask_ratio", [0.0, 0.3])
def test_lejepa_patch_mask_ratio_forward(patch_mask_ratio):
    torch.manual_seed(0)
    model = LeJEPA(
        encoder_name="vit_tiny_patch16_224",
        n_slices=8,
        n_points=5,
        pretrained=False,
        drop_path_rate=0.0,
        patch_mask_ratio=patch_mask_ratio,
    )

    assert model.patch_mask_ratio == patch_mask_ratio
    if patch_mask_ratio == 0.0:
        assert not hasattr(model.backbone, "masking")
    else:
        assert model.backbone.masking.mask_ratio == patch_mask_ratio
    _assert_training_forward(model)


def test_lejepa_patch_masking_eval_returns_embedding_without_masking():
    torch.manual_seed(0)
    model = LeJEPA(
        encoder_name="vit_tiny_patch16_224",
        n_slices=8,
        n_points=5,
        pretrained=False,
        drop_path_rate=0.0,
        patch_mask_ratio=0.3,
    )

    model.eval()
    images = torch.randn(2, 3, 224, 224)
    output = model(images=images)
    encoded = model.backbone(images)

    assert output.embedding.shape == (2, model.embed_dim)
    assert torch.isfinite(output.embedding).all()
    assert output.loss.item() == 0.0
    assert encoded.mask.sum().item() == 0.0
    assert (
        encoded.encoded.shape[1]
        == model.backbone.num_prefix_tokens + 14 * 14
    )


def test_lejepa_patch_masking_local_view_smaller_than_global_does_not_crash():
    torch.manual_seed(0)
    model = LeJEPA(
        encoder_name="vit_tiny_patch16_224",
        n_slices=8,
        n_points=5,
        pretrained=False,
        drop_path_rate=0.0,
        patch_mask_ratio=0.3,
    )

    _assert_training_forward(model)


@pytest.mark.parametrize("predictor", ["linear", "mlp"])
def test_lejepa_predictor_params_receive_gradients(predictor):
    torch.manual_seed(0)
    model = LeJEPA(
        encoder_name="vit_tiny_patch16_224",
        n_slices=8,
        n_points=5,
        pretrained=False,
        drop_path_rate=0.0,
        predictor=predictor,
    )
    output = _assert_training_forward(model)
    output.loss.backward()

    predictor_params = list(model.predictor.parameters())
    assert predictor_params
    assert any(
        param.grad is not None
        and torch.isfinite(param.grad).all()
        and param.grad.abs().sum() > 0
        for param in predictor_params
    )
