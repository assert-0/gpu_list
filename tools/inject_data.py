from bson import ObjectId

from model import GPUModel, GPUChip, GPUChipReference


def main():
    ad_102_id = ObjectId()
    ga_102_id = ObjectId()
    gh_100_id = ObjectId()
    navi_31_id = ObjectId()
    navi_23_id = ObjectId()
    chips = [
        GPUChip(
            _id=ad_102_id,
            chipName="AD102",
            architecture="Ada Lovelace",
            fab="TSMC 4N",
            transistors=76.3,
            dieSize=608.5,
        ),
        GPUChip(
            _id=ga_102_id,
            chipName="GA102",
            architecture="Ampere",
            fab="Samsung 8LPP",
            transistors=28.3,
            dieSize=628,
        ),
        GPUChip(
            _id=gh_100_id,
            chipName="GH100",
            architecture="Hopper",
            fab="TSMC 4N",
            transistors=80,
            dieSize=814,
        ),
        GPUChip(
            _id=navi_31_id,
            chipName="Navi 31",
            architecture="RDNA 3",
            fab="TSMC N5",
            transistors=57.7,
            dieSize=531,
        ),
        GPUChip(
            _id=navi_23_id,
            chipName="Navi 23",
            architecture="RDNA 2",
            fab="TSMC N7",
            transistors=11.06,
            dieSize=237,
        )
    ]
    for chip in chips:
        chip.save()

    gpu_models = [
        GPUModel(
            modelName="RTX 4090",
            manufacturer="NVIDIA",
            chip=GPUChipReference(id=ad_102_id),
            launchDate="2022-10-12",
            launchPrice="1599",
            memory=24,
            computeUnits=128,
            performance=82.6,
        ),
        GPUModel(
            modelName="RTX 6000 Ada",
            manufacturer="NVIDIA",
            chip=GPUChipReference(id=ad_102_id),
            launchDate="2022-12-03",
            launchPrice="6800",
            memory=48,
            computeUnits=142,
            performance=91.06,
        ),
        GPUModel(
            modelName="RTX 3090ti",
            manufacturer="NVIDIA",
            chip=GPUChipReference(id=ga_102_id),
            launchDate="2022-03-29",
            launchPrice="1999",
            memory=24,
            computeUnits=84,
            performance=40.6,
        ),
        GPUModel(
            modelName="RTX 3090",
            manufacturer="NVIDIA",
            chip=GPUChipReference(id=ga_102_id),
            launchDate="2020-09-24",
            launchPrice="1499",
            memory=24,
            computeUnits=82,
            performance=35.6,
        ),
        GPUModel(
            modelName="H100 GPU accelerator (PCIe)",
            manufacturer="NVIDIA",
            chip=GPUChipReference(id=gh_100_id),
            launchDate="2022-03-22",
            launchPrice="25000",
            memory=80,
            computeUnits=114,
            performance=51.2,
        ),
        GPUModel(
            modelName="Radeon RX 6650 XT",
            manufacturer="AMD",
            chip=GPUChipReference(id=navi_23_id),
            launchDate="2022-05-10",
            launchPrice="399",
            memory=8,
            computeUnits=32,
            performance=10.8,
        ),
        GPUModel(
            modelName="Radeon RX 6600 XT",
            manufacturer="AMD",
            chip=GPUChipReference(id=navi_23_id),
            launchDate="2021-08-11",
            launchPrice="379",
            memory=8,
            computeUnits=32,
            performance=10.6,
        ),
        GPUModel(
            modelName="Radeon Pro W6600",
            manufacturer="AMD",
            chip=GPUChipReference(id=navi_23_id),
            launchDate="2021-06-08",
            launchPrice="649",
            memory=8,
            computeUnits=28,
            performance=10.4,
        ),
        GPUModel(
            modelName="Radeon RX 7900 XT",
            manufacturer="AMD",
            chip=GPUChipReference(id=navi_31_id),
            launchDate="2022-12-13",
            launchPrice="899",
            memory=20,
            computeUnits=84,
            performance=51.6,
        ),
        GPUModel(
            modelName="Radeon Pro W7900",
            manufacturer="AMD",
            chip=GPUChipReference(id=navi_31_id),
            launchDate="2023-04-13",
            launchPrice="3999",
            memory=48,
            computeUnits=96,
            performance=61.3,
        ),
    ]

    for model in gpu_models:
        model.save()


if __name__ == '__main__':
    main()
