"""LeJEPA ablation specifications."""

from __future__ import annotations

from .common import AblationSpec


BASE_OVERRIDES = {
    "dataset_name": "inet100",
    "max_epochs": 50,
    "backbone": "vit_large_patch14_224",
    "batch_size": 512,
    "bstat_name": "epps_pulley",
    "bstat_num_slices": 1024,
    "bstat_t_max": 3.0,
    "bstat_n_points": 17,
    "bstat_lambda": 0.05,
    "embedding_dim": 512,
    "projector_dim": 512,
    "projector_arch": "MLP",
    "lr": 5e-4,
    "weight_decay": 5e-2,
    "teacher_student": False,
    "n_views": 8,
    "n_global_views": 2,
    "drop_path_rate": 0.1,
    "multi_crop": True,
    "resolution": 238,
    "local_resolution": 98,
    "patch_size": 14,
    "patch_mask_ratio": 0.3,
    "autostop": False,
}


def _check_timm_reg_token_support(model_name: str) -> tuple[bool, str]:
    try:
        import timm

        model = timm.create_model(
            model_name,
            pretrained=False,
            num_classes=0,
            reg_tokens=1,
        )
    except TypeError as exc:
        if "reg_tokens" in str(exc):
            return (
                False,
                f"{model_name} does not accept timm reg_tokens in this environment: {exc}",
            )
        return (
            False,
            f"{model_name} could not be checked for timm reg_tokens support: {exc}",
        )
    except Exception as exc:
        return (
            False,
            f"{model_name} could not be checked for timm reg_tokens support: {exc}",
        )

    actual_reg_tokens = getattr(model, "num_reg_tokens", None)
    if actual_reg_tokens == 1:
        return (
            True,
            f"{model_name} supports timm reg_tokens; num_reg_tokens={actual_reg_tokens}.",
        )
    return (
        False,
        f"{model_name} accepted reg_tokens but reported num_reg_tokens={actual_reg_tokens!r}.",
    )


_REG_TOKENS_SUPPORTED, _REG_TOKENS_SUPPORT_NOTE = _check_timm_reg_token_support(
    BASE_OVERRIDES["backbone"]
)
_REG_TOKENS_STATUS = "ready" if _REG_TOKENS_SUPPORTED else "needs_model_support"
_REG_TOKENS_REQUIRES = () if _REG_TOKENS_SUPPORTED else ("stable_timm_reg_tokens",)


SMOKE_OVERRIDES = {
    "dataset_name": "synthetic",
    "max_steps": 3,
    "batch_size": 4,
    "num_workers": 0,
    "backbone": "vit_tiny_patch16_224",
    "resolution": 224,
    "local_resolution": 96,
    "patch_size": 16,
    "bstat_num_slices": 16,
    "accelerator": "cpu",
    "devices": 1,
    "precision": 32,
}


TRAIN_ENTRYPOINT_SUPPORTED_KEYS = frozenset(
    {
        "dataset_name",
        "max_epochs",
        "max_steps",
        "batch_size",
        "num_workers",
        "backbone",
        "pretrained",
        "resolution",
        "local_resolution",
        "n_views",
        "n_global_views",
        "lr",
        "weight_decay",
        "precision",
        "accelerator",
        "devices",
        "drop_path_rate",
        "bstat_name",
        "bstat_lambda",
        "bstat_num_slices",
        "bstat_t_max",
        "bstat_n_points",
        "embedding_dim",
        "projector_dim",
        "projector_arch",
        "projector_hidden_dim",
        "projector_norm",
        "sigreg_target",
        "predictor",
        "predictor_hidden_dim",
        "predictor_norm",
        "reg_tokens",
        "aggregator",
        "teacher_student",
        "multi_crop",
        "patch_size",
        "patch_mask_ratio",
        "patch_mask_block_size",
        "patch_mask_crop_ratio",
        "autostop",
        "seed",
    }
)


ABLATIONS = (
    AblationSpec(
        key="epps",
        title="Epps-Pulley Parameters",
        question="How sensitive is SIGReg to the sliced Epps-Pulley integration grid?",
        priority=1,
        status="ready",
        grid={
            "bstat_num_slices": [512, 1024, 4096],
            "bstat_t_max": [1, 3, 5],
            "bstat_n_points": [5, 17, 41],
        },
        expected="Moderate grid sizes should be enough; very small grids may under-regularize.",
        notes=("Existing LeJEPA exposes n_slices, t_max, n_points, and lamb.",),
    ),
    AblationSpec(
        key="projector_dims",
        title="Projector Dimensions",
        question="How do projector input/output dimensions affect representation quality?",
        priority=2,
        status="needs_model_support",
        grid={
            "embedding_dim": [512, 2048],
            "projector_dim": [64, 128, 256, 512, 1024],
        },
        requires=("projector_dim_mapping_clarification",),
        expected="A medium projector dimension is likely best; extremely small heads may bottleneck SIGReg.",
        notes=(
            "Ported from the existing projector ablation plan as 10 configs.",
            "Current LeJEPA derives backbone embed_dim from timm, so embedding_dim needs clarification.",
        ),
    ),
    AblationSpec(
        key="reg_tokens",
        title="Register Tokens",
        question="Do ViT register tokens improve LeJEPA training or downstream features?",
        priority=3,
        status=_REG_TOKENS_STATUS,
        grid={"reg_tokens": [0, 1, 2, 4, 8]},
        requires=_REG_TOKENS_REQUIRES,
        expected="Small register-token counts may help; support depends on the selected timm ViT.",
        notes=(
            "LeJEPA passes positive reg_tokens into timm.create_model.",
            _REG_TOKENS_SUPPORT_NOTE,
        ),
    ),
    AblationSpec(
        key="views",
        title="Number of Views",
        question="How many total and global views are useful for LeJEPA?",
        priority=4,
        status="ready",
        cases=[
            {"n_views": 4, "n_global_views": 2, "batch_size": 256, "bstat_num_slices": 1000, "autostop": True},
            {"n_views": 6, "n_global_views": 2, "batch_size": 432, "bstat_num_slices": 1000, "autostop": True},
            {"n_views": 8, "n_global_views": 2, "batch_size": 512, "bstat_num_slices": 1000, "autostop": True},
            {"n_views": 10, "n_global_views": 2, "batch_size": 640, "bstat_num_slices": 1000, "autostop": True},
            {"n_views": 6, "n_global_views": 4, "batch_size": 384, "bstat_num_slices": 1000, "autostop": True},
            {"n_views": 8, "n_global_views": 4, "batch_size": 512, "bstat_num_slices": 1000, "autostop": True},
            {"n_views": 10, "n_global_views": 4, "batch_size": 600, "bstat_num_slices": 1000, "autostop": True},
            {"n_views": 4, "n_global_views": 1, "batch_size": 256, "bstat_num_slices": 1000, "autostop": False},
            {"n_views": 6, "n_global_views": 1, "batch_size": 384, "bstat_num_slices": 1000, "autostop": False},
            {"n_views": 8, "n_global_views": 1, "batch_size": 512, "bstat_num_slices": 1000, "autostop": False},
            {"n_views": 10, "n_global_views": 1, "batch_size": 600, "bstat_num_slices": 1000, "autostop": False},
        ],
        expected="More views may help up to a memory/optimization limit; global-view count tests the center estimate.",
        notes=("Uses explicit cases because batch_size is adjusted per view setting.",),
    ),
    AblationSpec(
        key="projector_depth",
        title="Projector Architecture",
        question="How many MLP layers are needed in the projector, and is a linear head enough?",
        priority=5,
        status="ready",
        grid={"projector_arch": ["Linear", "MLP2", "MLP", "MLP4"]},
        expected="A nonlinear projector is expected to outperform a linear head.",
        notes=("LeJEPA now builds Linear, MLP2, MLP, and MLP4 projectors.",),
    ),
    AblationSpec(
        key="patch_masking",
        title="Patch Masking Ratio",
        question="What patch masking ratio is optimal for invariance plus SIGReg?",
        priority=6,
        status="ready",
        grid={"patch_mask_ratio": [0.0, 0.1, 0.2, 0.3, 0.5, 0.7]},
        expected="A moderate mask ratio around 0.2-0.4 is expected to be best.",
        notes=("LeJEPA uses PatchMasking and MaskedEncoder when patch_mask_ratio > 0.",),
    ),
    AblationSpec(
        key="drop_path",
        title="Drop Path Rate",
        question="How sensitive is LeJEPA to stochastic depth regularization in ViT?",
        priority=7,
        status="ready",
        grid={"drop_path_rate": [0.0, 0.05, 0.1, 0.2, 0.4]},
        expected="Moderate drop path around 0.1-0.2 is expected to work best for ViT-L.",
        notes=("LeJEPA already forwards drop_path_rate to timm.create_model.",),
    ),
    AblationSpec(
        key="aggregation",
        title="Feature Aggregation",
        question="Which ViT output should feed the projector?",
        priority=8,
        status="ready",
        grid={"aggregator": ["cls", "mean", "cls_mean"]},
        expected="cls_mean or cls2 may provide richer training signals than cls alone.",
        notes=(
            "LeJEPA supports cls, mean, and cls_mean aggregation.",
            "cls2 remains blocked for a future phase because it needs intermediate features or hooks.",
        ),
    ),
    AblationSpec(
        key="sigreg_target",
        title="SIGReg Application Point",
        question="Should SIGReg regularize projector output, backbone embeddings, or both?",
        priority=9,
        status="ready",
        grid={"sigreg_target": ["proj", "embed", "both"]},
        expected="Projector-space SIGReg is expected to remain strongest.",
        notes=("LeJEPA supports projector, embedding, and averaged SIGReg targets.",),
    ),
    AblationSpec(
        key="predictor",
        title="Predictor Head",
        question="Does a BYOL/I-JEPA-style predictor help the invariance objective?",
        priority=10,
        status="ready",
        grid={"predictor": ["none", "linear", "mlp"]},
        expected="The no-predictor baseline is expected to be competitive.",
        notes=("Predictor output is used for invariance; SIGReg remains on projector output.",),
    ),
)


_SPEC_BY_KEY = {spec.key: spec for spec in ABLATIONS}


def list_specs() -> tuple[AblationSpec, ...]:
    """Return all specs sorted by priority."""

    return tuple(sorted(ABLATIONS, key=lambda spec: (spec.priority, spec.key)))


def get_spec(key: str) -> AblationSpec:
    """Return one spec by key."""

    try:
        return _SPEC_BY_KEY[key]
    except KeyError as exc:
        valid = ", ".join(spec.key for spec in list_specs())
        raise KeyError(f"unknown ablation {key!r}; valid keys: {valid}") from exc
