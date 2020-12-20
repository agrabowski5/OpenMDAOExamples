import openmdao.api as om
import numpy as np

#assign each variable it's own component

# Independent Variable
xComp = om.IndepVarComp('x')

#Implicit Variable created with a component
class yComp(om.ImplicitComponent):
    def setup(self):
        self.add_input('x',val = 1)
        self.add_input('z',val = 1)
        self.add_output('y',val = 1)
    def setup_partials(self):
        self.declare_partials(of='*',wrt='*')
    def apply_nonlinear(self, inputs, outputs, residuals):
        x = inputs['x']
        z = inputs['z']
        y = outputs['y']
        residuals['y'] = np.cos(x*y) - z*y

#Explicit Variable created with a component
class zComp(om.ExplicitComponent):
    def setup(self):
        self.add_input('y')
        self.add_output('z')

    def setup_partials(self):
        self.declare_partials('*', '*')

    def compute(self, inputs, outputs):
        y = inputs['y']
        outputs['z'] = np.sin(y)

if __name__ == '__main__':
    
    model = om.Group()
    model.add_subsystem('z', zComp())
    model.add_subsystem('y', yComp())
    model.add_subsystem('x', xComp)
    model.connect('y.y','z.y')
    model.connect('z.z','y.z')

    
    #model.linear_solver = om.DirectSolver()

    model.nonlinear_solver = om.NewtonSolver(solve_subsystems=True)
    model.nonlinear_solver.options['maxiter'] = 100
    model.nonlinear_solver.options['iprint'] = 2

    prob = om.Problem(model)
    prob.setup()

    prob.run_model()

    x = prob['y.x']
    y = prob['y.y']
    z = prob['y.z']

    print("X Value:", x)
    print("Y Value:", y)
    print("Z Value:", z)

    myAns = np.cos(x*y) -z*y 

    if (prob['y.z'] == np.sin(prob['y.y'])) & (abs(myAns) <= .00001):
        print('Passed')    
    else:
        print('Not Passed')
    

