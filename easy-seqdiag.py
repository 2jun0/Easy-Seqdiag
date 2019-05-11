from seqdiag import parser, builder, drawer
from blockdiag.utils.fontmap import FontMap
from blockdiag import utils
from preProcessor import convert_to_origin_seqdiag, pre_process, read_file_and_process
import sys

def draw_diag(path):

    read_file_and_process(path)
    diagram_definition = convert_to_origin_seqdiag()

    print('Converted definition : {}'.format(diagram_definition))

    tree = parser.parse_string(diagram_definition)
    diagram = builder.ScreenNodeBuilder.build(tree)

    fm = FontMap()
    fm.set_default_font('./malgun.ttf')

    draw = drawer.DiagramDraw('PNG', diagram, filename='{}.png'.format(path.split('/\\')[-1].split('.')[0]), fontmap=fm)
    draw.draw()
    draw.save()
    pass
def main(args):
    draw_diag(args[0])

if __name__ == '__main__':
    main(sys.argv[1:])
