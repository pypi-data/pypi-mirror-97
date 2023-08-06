"""Console script for glob_to_gif."""
import sys
import click
import glob
import imageio


@click.command()
@click.argument("input", type=click.STRING, nargs=1)
@click.argument("output", type=click.STRING, nargs=1)
@click.option("--fps", type=click.INT, default=30, help="Default: 30")
def main(input, output, fps):

    images = []

    print(f"Making gif from {len(glob.glob(input))} files found with {input}")

    for file_name in sorted(glob.glob(input)):
        images.append(imageio.imread(file_name))
    imageio.mimsave(output, images, fps=fps)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
