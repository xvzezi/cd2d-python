import Transform
import Geometry.Shape as Shape

class GameObject(object):
    def __init__(self):
        super(GameObject, self).__init__()
        self.geometry = None    # type: Shape.Shape
        self.tranform = None    # type: Transform.Transform
    
    def Init(self, geo, trans):
        # type: (Shape.Shape, Transform.Transform)->None
        self.geometry = geo 
        self.geometry.gameObject = self 
        self.tranform = trans
        self.tranform.gameObject = self 
