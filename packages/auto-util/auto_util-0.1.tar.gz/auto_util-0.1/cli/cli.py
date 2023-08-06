import click
from air.aircv.template_matching import TemplateMatching
from air.aircv.keypoint_matching import KAZEMatching, BRISKMatching, AKAZEMatching, ORBMatching
from air.aircv.keypoint_matching_contrib import SIFTMatching, SURFMatching, BRIEFMatching
from air.aircv.aircv import *

MATCHING_METHODS = {
    "tpl": TemplateMatching,
    "kaze": KAZEMatching,
    "brisk": BRISKMatching,
    "akaze": AKAZEMatching,
    "orb": ORBMatching,
    "sift": SIFTMatching,
    "surf": SURFMatching,
    "brief": BRIEFMatching,
}

OK = 0
Fail = -101
Error = -102


@click.command()
@click.option("--src", type=str, help="Source image path", required=True)
@click.option("--search", type=str, help="The path of the image to be matched", required=True)
@click.option("--threshold", type=float, default=0.7, help="Confidence threshold")
@click.option("--methods", multiple=True, default=["tpl", "surf", "brisk"],
              help="Matching algorithm, can pass in multiple [tpl,kaze,brisk,akaze,orb,sift,surf,brief]")
def match(src, search, threshold, methods):
    """
    Result:
    0 is Ok
    -101 is Fail
    -102 is Error
    """
    src_image = imread(src)
    search_image = imread(search)
    for method in methods:
        func = MATCHING_METHODS.get(method, None)
        if func is None:
            sys.stderr.write("Method not found:" + method)
            exit(Error)
            return
        else:
            ret = func(search_image, src_image, threshold=threshold).find_best_result()
            if ret:
                exit(OK)
                return
    sys.stderr.write("Image match fail")
    exit(Fail)
    return


@click.command('version')
def version():
    print('0.0.1')
    exit()


@click.group()
def main():
    pass


main.add_command(match)
main.add_command(version)


if __name__ == '__main__':
    main()
