"""Test fieldmap-less SDC-SyN."""
import os
import json
import pytest
from nipype.pipeline import engine as pe

from ..syn import init_syn_sdc_wf, init_syn_preprocessing_wf, _adjust_zooms


@pytest.mark.skipif(os.getenv("TRAVIS") == "true", reason="this is TravisCI")
@pytest.mark.skipif(os.getenv("GITHUB_ACTIONS") == "true", reason="this is GH Actions")
def test_syn_wf(tmpdir, datadir, workdir, outdir, sloppy_mode):
    """Build and run an SDC-SyN workflow."""
    derivs_path = datadir / "ds000054" / "derivatives"
    smriprep = derivs_path / "smriprep-0.6" / "sub-100185" / "anat"

    wf = pe.Workflow(name="test_syn")

    prep_wf = init_syn_preprocessing_wf(
        omp_nthreads=4,
        debug=sloppy_mode,
        auto_bold_nss=True,
        t1w_inversion=True,
    )
    prep_wf.inputs.inputnode.in_epis = [
        str(
            datadir
            / "ds000054"
            / "sub-100185"
            / "func"
            / "sub-100185_task-machinegame_run-01_bold.nii.gz"
        ),
        str(
            datadir
            / "ds000054"
            / "sub-100185"
            / "func"
            / "sub-100185_task-machinegame_run-02_bold.nii.gz"
        ),
    ]
    prep_wf.inputs.inputnode.in_meta = [
        json.loads((datadir / "ds000054" / "task-machinegame_bold.json").read_text()),
    ] * 2
    prep_wf.inputs.inputnode.std2anat_xfm = str(
        smriprep / "sub-100185_from-MNI152NLin2009cAsym_to-T1w_mode-image_xfm.h5"
    )
    prep_wf.inputs.inputnode.in_anat = str(
        smriprep / "sub-100185_desc-preproc_T1w.nii.gz"
    )
    prep_wf.inputs.inputnode.mask_anat = str(
        smriprep / "sub-100185_desc-brain_mask.nii.gz"
    )

    syn_wf = init_syn_sdc_wf(debug=sloppy_mode, omp_nthreads=4)

    # fmt: off
    wf.connect([
        (prep_wf, syn_wf, [
            ("outputnode.epi_ref", "inputnode.epi_ref"),
            ("outputnode.epi_mask", "inputnode.epi_mask"),
            ("outputnode.anat_ref", "inputnode.anat_ref"),
            ("outputnode.anat_mask", "inputnode.anat_mask"),
            ("outputnode.sd_prior", "inputnode.sd_prior"),
        ]),
    ])
    # fmt: on

    if outdir:
        from ...outputs import init_fmap_derivatives_wf, init_fmap_reports_wf

        outdir = outdir / "unittests" / "test_syn"
        fmap_derivatives_wf = init_fmap_derivatives_wf(
            output_dir=str(outdir),
            write_coeff=True,
            bids_fmap_id="sdcsyn",
        )
        fmap_derivatives_wf.inputs.inputnode.source_files = [
            str(
                derivs_path
                / "sdcflows-tests"
                / "sub-100185_task-machinegame_run-1_boldref.nii.gz"
            )
        ]
        fmap_derivatives_wf.inputs.inputnode.fmap_meta = {
            "PhaseEncodingDirection": "j-"
        }

        fmap_reports_wf = init_fmap_reports_wf(
            output_dir=str(outdir),
            fmap_type="sdcsyn",
        )
        fmap_reports_wf.inputs.inputnode.source_files = [
            str(
                derivs_path
                / "sdcflows-tests"
                / "sub-100185_task-machinegame_run-1_boldref.nii.gz"
            )
        ]

        # fmt: off
        wf.connect([
            (syn_wf, fmap_reports_wf, [
                ("outputnode.fmap", "inputnode.fieldmap"),
                ("outputnode.fmap_ref", "inputnode.fmap_ref"),
                ("outputnode.fmap_mask", "inputnode.fmap_mask")]),
            (syn_wf, fmap_derivatives_wf, [
                ("outputnode.fmap", "inputnode.fieldmap"),
                ("outputnode.fmap_ref", "inputnode.fmap_ref"),
                ("outputnode.fmap_coeff", "inputnode.fmap_coeff"),
            ]),
        ])
        # fmt: on

    if workdir:
        wf.base_dir = str(workdir)

    wf.run(plugin="Linear")


@pytest.mark.parametrize("ants_version", ["2.2.0", "2.1.0", None])
def test_syn_wf_version(monkeypatch, ants_version):
    """Ensure errors are triggered with ANTs < 2.2."""
    from niworkflows.interfaces.fixes import FixHeaderRegistration as Registration

    monkeypatch.setattr(Registration, "version", ants_version)
    if ants_version == "2.1.0":
        with pytest.raises(RuntimeError):
            init_syn_sdc_wf(debug=True, omp_nthreads=4)
    else:
        wf = init_syn_sdc_wf(debug=True, omp_nthreads=4)
        assert (ants_version or "version unknown") in wf.__desc__


@pytest.mark.parametrize(
    "anat_res,epi_res,retval",
    [
        ((1.0, 1.0, 1.0), (2.0, 2.0, 2.0), (1.8, 1.8, 1.8)),
        ((1.8, 1.8, 1.8), (2.0, 2.0, 2.0), (1.9, 1.9, 1.9)),
        ((1.5, 1.5, 1.5), (1.8, 1.8, 1.8), (1.8, 1.8, 1.8)),
        ((1.8, 1.8, 1.8), (2.5, 2.5, 2.5), (2.15, 2.15, 2.15)),
    ],
)
def test_adjust_zooms(anat_res, epi_res, retval, tmpdir, datadir):
    """Exercise the adjust zooms function node."""
    import numpy as np
    import nibabel as nb

    tmpdir.chdir()

    nb.Nifti1Image(
        np.zeros((10, 10, 10)),
        np.diag(list(anat_res) + [1]),
        None,
    ).to_filename("anat.nii.gz")
    nb.Nifti1Image(
        np.zeros((10, 10, 10)),
        np.diag(list(epi_res) + [1]),
        None,
    ).to_filename("epi.nii.gz")

    assert _adjust_zooms("anat.nii.gz", "epi.nii.gz") == retval
