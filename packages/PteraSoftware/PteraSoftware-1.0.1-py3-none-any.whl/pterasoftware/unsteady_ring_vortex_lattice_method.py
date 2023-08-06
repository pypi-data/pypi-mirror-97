""" This module contains the class definition of this package's unsteady ring vortex lattice solver.

This module contains the following classes:
    UnsteadyRingVortexLatticeMethodSolver: This is an aerodynamics solver that uses an unsteady ring vortex lattice
                                           method.

This module contains the following exceptions:
    None

This module contains the following functions:
    None
"""

import copy as copy

import numpy as np

import pterasoftware as ps


class UnsteadyRingVortexLatticeMethodSolver:
    """ This is an aerodynamics solver that uses an unsteady ring vortex lattice method.

    This class contains the following public methods:
        run: This method runs the solver on the unsteady problem.
        initialize_panel_vortices: This method calculates the locations of an airplane's bound vortex vertices, and then
                                   initializes its panels' bound vortices.
        collapse_geometry: This method converts attributes of the problem's geometry into 1D ndarrays. This facilitates
                           vectorization, which speeds up the solver.
        calculate_wing_wing_influences: This method finds the matrix of wing-wing influence coefficients associated with
                                        this airplane's geometry.
        calculate_freestream_wing_influences: This method finds the vector of freestream-wing influences associated with
                                              the problem at this time step.
        calculate_wake_wing_influences: This method finds the vector of the wake-wing influences associated with the
                                        problem at this time step.
        calculate_vortex_strengths: This method solves for each panel's vortex strength.
        calculate_solution_velocity: This function takes in a group of points. At every point, it finds the induced
                                     velocity due to every vortex and the freestream velocity.
        calculate_near_field_forces_and_moments: This method finds the the forces and moments calculated from the near
                                                 field.
        calculate_streamlines: This method calculates the location of the streamlines coming off the back of the wings.
        populate_next_airplanes_wake: This method updates the next time step's airplane's wake.
        populate_next_airplanes_wake_vortex_vertices: This method populates the locations of the next airplane's wake
                                                      vortex vertices.
        populate_next_airplanes_wake_vortices: This method populates the locations of the next airplane's wake vortices.
        calculate_current_flapping_velocities_at_collocation_points: This method gets the velocity due to flapping at
                                                                     all of the current airplane's collocation points.
        calculate_current_flapping_velocities_at_right_leg_centers: This method gets the velocity due to flapping at the
                                                                    centers of the current airplane's bound ring
                                                                    vortices' right legs.
        calculate_current_flapping_velocities_at_front_leg_centers: This method gets the velocity due to flapping at the
                                                                    centers of the current airplane's bound ring
                                                                    vortices' front legs.
        calculate_current_flapping_velocities_at_left_leg_centers: This method gets the velocity due to flapping at the
                                                                   centers of the current airplane's bound ring
                                                                   vortices' left legs.


    This class contains the following class attributes:
        None

    Subclassing:
        This class is not meant to be subclassed.
    """

    def __init__(self, unsteady_problem):
        """ This is the initialization method.

        :param unsteady_problem: UnsteadyProblem
            This is the unsteady problem to be solved.
        """

        # Initialize this solution's attributes.
        self.num_steps = unsteady_problem.num_steps
        self.delta_time = unsteady_problem.delta_time
        self.steady_problems = unsteady_problem.steady_problems

        # Initialize attributes to hold aerodynamic data that pertains to this problem.
        self.current_step = None
        self.current_airplane = None
        self.current_operating_point = None
        self.current_freestream_velocity_geometry_axes = None
        self.current_wing_wing_influences = None
        self.vectorized_current_wing_wing_influences = None
        self.current_freestream_wing_influences = None
        self.vectorized_current_freestream_wing_influences = None
        self.current_wake_wing_influences = None
        self.vectorized_current_wake_wing_influences = None
        self.current_vortex_strengths = None
        self.vectorized_current_vortex_strengths = None
        self.streamline_points = None

        # Initialize attributes to hold geometric data that pertains to this problem.
        self.panels = None
        self.panel_normal_directions = None
        self.panel_areas = None
        self.panel_centers = None
        self.panel_collocation_points = None
        self.panel_back_right_vortex_vertices = None
        self.panel_front_right_vortex_vertices = None
        self.panel_front_left_vortex_vertices = None
        self.panel_back_left_vortex_vertices = None
        self.panel_right_vortex_centers = None
        self.panel_right_vortex_vectors = None
        self.panel_front_vortex_centers = None
        self.panel_front_vortex_vectors = None
        self.panel_left_vortex_centers = None
        self.panel_left_vortex_vectors = None
        self.panel_back_vortex_centers = None
        self.panel_back_vortex_vectors = None
        self.seed_points = None

        # Initialize variables to hold aerodynamic data that pertains details about this panel's location on its wing.
        self.panel_is_trailing_edge = None
        self.panel_is_leading_edge = None
        self.panel_is_left_edge = None
        self.panel_is_right_edge = None

        # Initialize variables to hold aerodynamic data that pertains to this problem's last time step.
        self.last_panel_collocation_points = None
        self.last_panel_vortex_strengths = None
        self.last_panel_back_right_vortex_vertices = None
        self.last_panel_front_right_vortex_vertices = None
        self.last_panel_front_left_vortex_vertices = None
        self.last_panel_back_left_vortex_vertices = None
        self.last_panel_right_vortex_centers = None
        self.last_panel_front_vortex_centers = None
        self.last_panel_left_vortex_centers = None
        self.last_panel_back_vortex_centers = None

        # Initialize variables to hold aerodynamic data that pertains to this problem's wake.
        self.wake_ring_vortex_strengths = None
        self.wake_ring_vortex_front_right_vertices = None
        self.wake_ring_vortex_front_left_vertices = None
        self.wake_ring_vortex_back_left_vertices = None
        self.wake_ring_vortex_back_right_vertices = None

    def run(self, verbose=True, prescribed_wake=True):
        """ This method runs the solver on the unsteady problem.

        :param verbose: Bool, optional
            This parameter determines if the solver prints output to the console and opens a visualization. It's default
            value is True.
        :param prescribed_wake: Bool, optional
            This parameter determines if the solver uses a prescribed wake model. If false it will use a free-wake,
            which may be more accurate but will make the solver significantly slower. The default is True.
        :return: None
        """

        # Initialize all the airplanes' panels' vortices.
        if verbose:
            print("Initializing all airplanes' panel vortices.")
        self.initialize_panel_vortices()

        # Iterate through the time steps.
        for step in range(self.num_steps):

            # Save attributes to hold the current step, airplane, and operating point.
            self.current_step = step
            self.current_airplane = self.steady_problems[self.current_step].airplane
            self.current_operating_point = self.steady_problems[
                self.current_step
            ].operating_point
            self.current_freestream_velocity_geometry_axes = (
                self.current_operating_point.calculate_freestream_velocity_geometry_axes()
            )
            if verbose:
                print(
                    "\nBeginning time step "
                    + str(self.current_step)
                    + " out of "
                    + str(self.num_steps - 1)
                    + "."
                )

            # Initialize attributes to hold aerodynamic data that pertains to this problem.
            self.current_wing_wing_influences = np.zeros(
                (self.current_airplane.num_panels, self.current_airplane.num_panels)
            )
            self.vectorized_current_wing_wing_influences = np.zeros(
                (self.current_airplane.num_panels, self.current_airplane.num_panels)
            )
            self.current_freestream_velocity_geometry_axes = (
                self.current_operating_point.calculate_freestream_velocity_geometry_axes()
            )
            self.current_freestream_wing_influences = np.zeros(
                self.current_airplane.num_panels
            )
            self.vectorized_current_freestream_wing_influences = np.zeros(
                self.current_airplane.num_panels
            )
            self.current_wake_wing_influences = np.zeros(
                self.current_airplane.num_panels
            )
            self.vectorized_current_wake_wing_influences = np.zeros(
                self.current_airplane.num_panels
            )
            self.current_vortex_strengths = np.ones(self.current_airplane.num_panels)
            self.vectorized_current_vortex_strengths = np.ones(
                self.current_airplane.num_panels
            )

            # Initialize attributes to hold geometric data that pertains to this problem.
            self.panels = np.empty(self.current_airplane.num_panels, dtype=object)
            self.panel_normal_directions = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_areas = np.zeros(self.current_airplane.num_panels)
            self.panel_centers = np.zeros((self.current_airplane.num_panels, 3))
            self.panel_collocation_points = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_back_right_vortex_vertices = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_front_right_vortex_vertices = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_front_left_vortex_vertices = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_back_left_vortex_vertices = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_right_vortex_centers = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_right_vortex_vectors = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_front_vortex_centers = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_front_vortex_vectors = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_left_vortex_centers = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_left_vortex_vectors = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_back_vortex_centers = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.panel_back_vortex_vectors = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.seed_points = np.empty((0, 3))

            # Initialize variables to hold details about this panel's location on its wing.
            self.panel_is_trailing_edge = np.zeros(
                self.current_airplane.num_panels, dtype=bool
            )
            self.panel_is_leading_edge = np.zeros(
                self.current_airplane.num_panels, dtype=bool
            )
            self.panel_is_left_edge = np.zeros(
                self.current_airplane.num_panels, dtype=bool
            )
            self.panel_is_right_edge = np.zeros(
                self.current_airplane.num_panels, dtype=bool
            )

            # Initialize variables to hold details about the last airplane's panels.
            self.last_panel_collocation_points = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.last_panel_vortex_strengths = np.zeros(
                self.current_airplane.num_panels
            )
            self.last_panel_back_right_vortex_vertices = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.last_panel_front_right_vortex_vertices = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.last_panel_front_left_vortex_vertices = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.last_panel_back_left_vortex_vertices = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.last_panel_right_vortex_centers = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.last_panel_front_vortex_centers = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.last_panel_left_vortex_centers = np.zeros(
                (self.current_airplane.num_panels, 3)
            )
            self.last_panel_back_vortex_centers = np.zeros(
                (self.current_airplane.num_panels, 3)
            )

            self.wake_ring_vortex_strengths = np.empty(0)
            self.wake_ring_vortex_front_right_vertices = np.empty((0, 3))
            self.wake_ring_vortex_front_left_vertices = np.empty((0, 3))
            self.wake_ring_vortex_back_left_vertices = np.empty((0, 3))
            self.wake_ring_vortex_back_right_vertices = np.empty((0, 3))

            # Collapse this problem's geometry matrices into 1D ndarrays of attributes.
            if verbose:
                print("Collapsing geometry.")
            self.collapse_geometry()

            # Find the matrix of wing-wing influence coefficients associated with this current_airplane's geometry.
            if verbose:
                print("Calculating the wing-wing influences.")
            self.calculate_wing_wing_influences()

            # Find the vector of freestream-wing influence coefficients associated with this problem.
            if verbose:
                print("Calculating the freestream-wing influences.")
            self.calculate_freestream_wing_influences()

            # Find the vector of wake-wing influence coefficients associated with this problem.
            if verbose:
                print("Calculating the wake-wing influences.")
            self.calculate_wake_wing_influences()

            # Solve for each panel's vortex strength.
            if verbose:
                print("Calculating vortex strengths.")
            self.calculate_vortex_strengths()

            # Solve for the near field forces and moments on each panel.
            if verbose:
                print("Calculating near field forces.")
            self.calculate_near_field_forces_and_moments()

            # Solve for the near field forces and moments on each panel.
            if verbose:
                print("Shedding wake vortices.")
            self.populate_next_airplanes_wake(prescribed_wake=prescribed_wake)

        # Solve for the location of the streamlines coming off the back of the wings.
        if verbose:
            print("\nCalculating streamlines.")
        self.calculate_streamlines()

    def initialize_panel_vortices(self):
        """ This method calculates the locations every problem's airplane's bound vortex vertices, and then initializes
        its panels' bound vortices.

        Every panel has a ring vortex, which is a quadrangle whose front vortex leg is at the panel's quarter chord.
        The left and right vortex legs run along the panel's left and right legs. If the panel is not along the
        trailing edge, they extend backwards and meet the back vortex leg at a length of one quarter of the rear
        panel's chord back from the rear panel's front leg. Otherwise, they extend back backwards and meet the back
        vortex leg at a length of one quarter of the current panel's chord back from the current panel's back leg.

        :return: None
        """

        # Iterate through all the steady problem objects.
        for steady_problem in self.steady_problems:

            # Get the freestream velocity at this time step's problem.
            this_freestream_velocity_geometry_axes = (
                steady_problem.operating_point.calculate_freestream_velocity_geometry_axes()
            )

            # Iterate through this problem's airplane's wings.
            for wing in steady_problem.airplane.wings:

                # Iterate through the wing's chordwise and spanwise positions.
                for chordwise_position in range(wing.num_chordwise_panels):
                    for spanwise_position in range(wing.num_spanwise_panels):

                        # Get the panel object from the wing's list of panels.
                        panel = wing.panels[chordwise_position, spanwise_position]

                        # Find the location of the panel's front left and right vortex vertices.
                        front_left_vortex_vertex = panel.front_left_vortex_vertex
                        front_right_vortex_vertex = panel.front_right_vortex_vertex

                        # Define the back left and right vortex vertices based on whether the panel is along the
                        # trailing edge or not.
                        if not panel.is_trailing_edge:
                            next_chordwise_panel = wing.panels[
                                chordwise_position + 1, spanwise_position
                            ]
                            back_left_vortex_vertex = (
                                next_chordwise_panel.front_left_vortex_vertex
                            )
                            back_right_vortex_vertex = (
                                next_chordwise_panel.front_right_vortex_vertex
                            )
                        else:
                            # As these vertices are directly behind the trailing edge, they are spaced back from their
                            # panel's vertex by one quarter the distance traveled during a time step. This is to more
                            # accurately predict drag. More information can be found on pages 37-39 of "Modeling of
                            # aerodynamic forces in flapping flight with the Unsteady Vortex Lattice Method" by Thomas
                            # Lambert.
                            back_left_vortex_vertex = (
                                front_left_vortex_vertex
                                + (panel.back_left_vertex - panel.front_left_vertex)
                                + this_freestream_velocity_geometry_axes
                                * self.delta_time
                                * 0.25
                            )
                            back_right_vortex_vertex = (
                                front_right_vortex_vertex
                                + (panel.back_right_vertex - panel.front_right_vertex)
                                + this_freestream_velocity_geometry_axes
                                * self.delta_time
                                * 0.25
                            )

                        # Initialize the panel's ring vortex.
                        panel.ring_vortex = ps.aerodynamics.RingVortex(
                            front_right_vertex=front_right_vortex_vertex,
                            front_left_vertex=front_left_vortex_vertex,
                            back_left_vertex=back_left_vortex_vertex,
                            back_right_vertex=back_right_vortex_vertex,
                            strength=None,
                        )

    def collapse_geometry(self):
        """ This method converts attributes of the problem's geometry into 1D ndarrays. This facilitates vectorization,
        which speeds up the solver.

        :return: None
        """

        # Initialize a variable to hold the global position of the panel as we iterate through them.
        global_panel_position = 0

        # Iterate through the current airplane's wings.
        for wing in self.current_airplane.wings:

            # Convert this wing's 2D ndarray of panels into a 1D ndarray.
            panels = np.ravel(wing.panels)
            wake_ring_vortices = np.ravel(wing.wake_ring_vortices)

            # Iterate through the 1D ndarray of this wing's panels.
            for panel in panels:

                # Update the solver's list of attributes with this panel's attributes.
                self.panels[global_panel_position] = panel
                self.panel_normal_directions[
                    global_panel_position, :
                ] = panel.normal_direction
                self.panel_areas[global_panel_position] = panel.area
                self.panel_centers[global_panel_position] = panel.center
                self.panel_collocation_points[
                    global_panel_position, :
                ] = panel.collocation_point
                self.panel_back_right_vortex_vertices[
                    global_panel_position, :
                ] = panel.ring_vortex.right_leg.origin
                self.panel_front_right_vortex_vertices[
                    global_panel_position, :
                ] = panel.ring_vortex.right_leg.termination
                self.panel_front_left_vortex_vertices[
                    global_panel_position, :
                ] = panel.ring_vortex.left_leg.origin
                self.panel_back_left_vortex_vertices[
                    global_panel_position, :
                ] = panel.ring_vortex.left_leg.termination
                self.panel_right_vortex_centers[
                    global_panel_position, :
                ] = panel.ring_vortex.right_leg.center
                self.panel_right_vortex_vectors[
                    global_panel_position, :
                ] = panel.ring_vortex.right_leg.vector
                self.panel_front_vortex_centers[
                    global_panel_position, :
                ] = panel.ring_vortex.front_leg.center
                self.panel_front_vortex_vectors[
                    global_panel_position, :
                ] = panel.ring_vortex.front_leg.vector
                self.panel_left_vortex_centers[
                    global_panel_position, :
                ] = panel.ring_vortex.left_leg.center
                self.panel_left_vortex_vectors[
                    global_panel_position, :
                ] = panel.ring_vortex.left_leg.vector
                self.panel_back_vortex_centers[
                    global_panel_position, :
                ] = panel.ring_vortex.back_leg.center
                self.panel_back_vortex_vectors[
                    global_panel_position, :
                ] = panel.ring_vortex.back_leg.vector
                self.panel_is_trailing_edge[
                    global_panel_position
                ] = panel.is_trailing_edge
                self.panel_is_leading_edge[
                    global_panel_position
                ] = panel.is_leading_edge
                self.panel_is_right_edge[global_panel_position] = panel.is_right_edge
                self.panel_is_left_edge[global_panel_position] = panel.is_left_edge

                # Check if this panel is on the trailing edge.
                if panel.is_trailing_edge:
                    # If it is, calculate it's streamline seed point and add it to the solver's ndarray of seed points.
                    self.seed_points = np.vstack(
                        (
                            self.seed_points,
                            panel.back_left_vertex
                            + 0.5 * (panel.back_right_vertex - panel.back_left_vertex),
                        )
                    )

                # Increment the global panel position.
                global_panel_position += 1

            for wake_ring_vortex in wake_ring_vortices:
                self.wake_ring_vortex_strengths = np.hstack(
                    (self.wake_ring_vortex_strengths, wake_ring_vortex.strength)
                )
                self.wake_ring_vortex_front_right_vertices = np.vstack(
                    (
                        self.wake_ring_vortex_front_right_vertices,
                        wake_ring_vortex.front_right_vertex,
                    )
                )
                self.wake_ring_vortex_front_left_vertices = np.vstack(
                    (
                        self.wake_ring_vortex_front_left_vertices,
                        wake_ring_vortex.front_left_vertex,
                    )
                )
                self.wake_ring_vortex_back_left_vertices = np.vstack(
                    (
                        self.wake_ring_vortex_back_left_vertices,
                        wake_ring_vortex.back_left_vertex,
                    )
                )
                self.wake_ring_vortex_back_right_vertices = np.vstack(
                    (
                        self.wake_ring_vortex_back_right_vertices,
                        wake_ring_vortex.back_right_vertex,
                    )
                )

        # Initialize a variable to hold the global position of the panel as we iterate through them.
        global_panel_position = 0

        if self.current_step > 0:

            last_airplane = self.steady_problems[self.current_step - 1].airplane

            # Iterate through the current airplane's wings.
            for wing in last_airplane.wings:

                # Convert this wing's 2D ndarray of panels into a 1D ndarray.
                panels = np.ravel(wing.panels)

                # Iterate through the 1D ndarray of this wing's panels.
                for panel in panels:
                    # Update the solver's list of attributes with this panel's attributes.
                    self.last_panel_collocation_points[
                        global_panel_position, :
                    ] = panel.collocation_point

                    self.last_panel_vortex_strengths[
                        global_panel_position
                    ] = panel.ring_vortex.strength

                    self.last_panel_back_right_vortex_vertices[
                        global_panel_position, :
                    ] = panel.ring_vortex.right_leg.origin

                    self.last_panel_front_right_vortex_vertices[
                        global_panel_position, :
                    ] = panel.ring_vortex.right_leg.termination

                    self.last_panel_front_left_vortex_vertices[
                        global_panel_position, :
                    ] = panel.ring_vortex.left_leg.origin

                    self.last_panel_back_left_vortex_vertices[
                        global_panel_position, :
                    ] = panel.ring_vortex.left_leg.termination

                    self.last_panel_right_vortex_centers[
                        global_panel_position, :
                    ] = panel.ring_vortex.right_leg.center

                    self.last_panel_front_vortex_centers[
                        global_panel_position, :
                    ] = panel.ring_vortex.front_leg.center

                    self.last_panel_left_vortex_centers[
                        global_panel_position, :
                    ] = panel.ring_vortex.left_leg.center

                    self.last_panel_back_vortex_centers[
                        global_panel_position, :
                    ] = panel.ring_vortex.back_leg.center

                    # Increment the global panel position.
                    global_panel_position += 1

    def calculate_wing_wing_influences(self):
        """ This method finds the matrix of wing-wing influence coefficients associated with this airplane's geometry.

        :return: None
        """

        # Find the matrix of normalized velocities induced at every panel's collocation point by every panel's ring
        # vortex. The answer is normalized because the solver's vortex strength list was initialized to all ones. This
        # will be updated once the correct vortex strength's are calculated.
        total_influences = ps.aerodynamics.calculate_velocity_induced_by_ring_vortices(
            points=self.panel_collocation_points,
            back_right_vortex_vertices=self.panel_back_right_vortex_vertices,
            front_right_vortex_vertices=self.panel_front_right_vortex_vertices,
            front_left_vortex_vertices=self.panel_front_left_vortex_vertices,
            back_left_vortex_vertices=self.panel_back_left_vortex_vertices,
            strengths=self.current_vortex_strengths,
            collapse=False,
        )

        # Take the batch dot product of the normalized velocities with each panel's normal direction. This is now the
        # problem's matrix of wing-wing influence coefficients.
        self.current_wing_wing_influences = np.einsum(
            "...k,...k->...",
            total_influences,
            np.expand_dims(self.panel_normal_directions, axis=1),
        )

    def calculate_freestream_wing_influences(self):
        """ This method finds the vector of freestream-wing influence coefficients associated with this problem.

        Note: This method also includes the influence due to flapping at every collocation point in the freestream-wing
              influence vector.

        :return: None
        """

        # Find the normal components of the freestream velocity on every panel by taking a batch dot product.
        freestream_influences = np.einsum(
            "ij,j->i",
            self.panel_normal_directions,
            self.current_freestream_velocity_geometry_axes,
        )

        # Get the current flapping velocities at every collocation point.
        current_flapping_velocities_at_collocation_points = (
            self.calculate_current_flapping_velocities_at_collocation_points()
        )

        # Find the normal components of every panel's flapping velocities at their collocation points by taking a batch
        # dot product.
        flapping_influences = np.einsum(
            "ij,ij->i",
            self.panel_normal_directions,
            current_flapping_velocities_at_collocation_points,
        )

        # Calculate the total current freestream-wing influences by summing the freestream influences and the
        # flapping influences.
        self.current_freestream_wing_influences = (
            freestream_influences + flapping_influences
        )

    def calculate_wake_wing_influences(self):
        """ This method finds the vector of the wake-wing influences associated with the problem at this time step.

        Note: If the current time step is the first time step, no wake has yet been shed, and this method will set the
              current wake-wing influence vector to all zeros.

        :return: None
        """

        # Check if this time step is not the first time step.
        if self.current_step > 0:

            # Get the wake induced velocities. This is a (M x 3) ndarray with the x, y, and z components of the velocity
            # induced by the entire wake at each of the M panels.
            wake_induced_velocities = ps.aerodynamics.calculate_velocity_induced_by_ring_vortices(
                points=self.panel_collocation_points,
                back_right_vortex_vertices=self.wake_ring_vortex_back_right_vertices,
                front_right_vortex_vertices=self.wake_ring_vortex_front_right_vertices,
                front_left_vortex_vertices=self.wake_ring_vortex_front_left_vertices,
                back_left_vortex_vertices=self.wake_ring_vortex_back_left_vertices,
                strengths=self.wake_ring_vortex_strengths,
                collapse=True,
            )

            # Set the current wake-wing influences to the normal component of the wake induced velocities at each panel.
            self.current_wake_wing_influences = np.einsum(
                "ij,ij->i", wake_induced_velocities, self.panel_normal_directions
            )

        else:

            # If this is the first time step, set the current wake-wing influences to zero everywhere, as there is no
            # wake yet.
            self.current_wake_wing_influences = np.zeros(
                self.current_airplane.num_panels
            )

    def calculate_vortex_strengths(self):
        """ This method solves for each panel's vortex strength.

        :return: None
        """

        # Solve for the strength of each panel's vortex.
        self.current_vortex_strengths = np.linalg.solve(
            self.current_wing_wing_influences,
            -self.current_wake_wing_influences
            - self.current_freestream_wing_influences,
        )

        # Iterate through the panels and update their vortex strengths.
        for panel_num in range(self.panels.size):
            # Get the panel at this location.
            panel = self.panels[panel_num]

            # Update this panel's ring vortex strength.
            panel.ring_vortex.update_strength(self.current_vortex_strengths[panel_num])

    def calculate_solution_velocity(self, points):
        """ This function takes in a group of points. At every point, it finds the induced velocity due to every vortex
        and the freestream velocity.

        Note: The velocity calculated by this method is in geometry axes. Also, this method assumes that the correct
              vortex strengths have already been calculated. This method also does not include the velocity due to
              flapping at any of the points provided, as it has no way of knowing if any of the points lie on panels.

        This method uses vectorization, and therefore is much faster for batch operations than using the vortex objects'
        class methods for calculating induced velocity.

        :param points: 2D ndarray of floats
            This variable is an ndarray of shape (N x 3), where N is the number of points. Each row contains the x, y,
            and z float coordinates of that point's position in meters.
        :return solution_velocities: 2D ndarray of floats
            The output is the summed effects from every vortex, and from the freestream on a given point. The result
            will be of shape (N x 3), where each row identifies the velocity at a point. The results units are meters
            per second.
        """

        # Find the vector of velocities induced at every point by every panel's ring vortex. The effect of every ring
        # vortex on each point will be summed.
        ring_vortex_velocities = ps.aerodynamics.calculate_velocity_induced_by_ring_vortices(
            points=points,
            back_right_vortex_vertices=self.panel_back_right_vortex_vertices,
            front_right_vortex_vertices=self.panel_front_right_vortex_vertices,
            front_left_vortex_vertices=self.panel_front_left_vortex_vertices,
            back_left_vortex_vertices=self.panel_back_left_vortex_vertices,
            strengths=self.current_vortex_strengths,
            collapse=True,
        )

        # Find the vector of velocities induced at every point by every wake ring vortex. The effect of every wake ring
        # vortex on each point will be summed.
        wake_ring_vortex_velocities = ps.aerodynamics.calculate_velocity_induced_by_ring_vortices(
            points=points,
            back_right_vortex_vertices=self.wake_ring_vortex_back_right_vertices,
            front_right_vortex_vertices=self.wake_ring_vortex_front_right_vertices,
            front_left_vortex_vertices=self.wake_ring_vortex_front_left_vertices,
            back_left_vortex_vertices=self.wake_ring_vortex_back_left_vertices,
            strengths=self.wake_ring_vortex_strengths,
            collapse=True,
        )

        # Find the total influence of the vortices, which is the sum of the influence due to the bound ring vortices and
        # the wake ring vortices.
        total_vortex_velocities = ring_vortex_velocities + wake_ring_vortex_velocities

        # Calculate and return the solution velocities, which is the sum of the velocities induced by the vortices and
        # freestream at every point.
        solution_velocities = (
            total_vortex_velocities + self.current_freestream_velocity_geometry_axes
        )
        return solution_velocities

    def calculate_near_field_forces_and_moments(self):
        """ This method finds the the forces and moments calculated from the near field.

        Citation:
            This method uses logic described on pages 9-11 of "Modeling of aerodynamic forces in flapping flight with
            the Unsteady Vortex Lattice Method" by Thomas Lambert.

        Note: The forces and moments calculated are in geometry axes. The moment is about the airplane's reference
                point, which should be at the center of gravity. The units are Newtons and Newton-meters.

        :return: None
        """

        # Initialize a variable to hold the global panel position as the panel's are iterate through.
        global_panel_position = 0

        # Initialize three lists of variables, which will hold the effective strength of the line vortices comprising
        # each panel's ring vortex.
        effective_right_vortex_line_strengths = np.zeros(
            self.current_airplane.num_panels
        )
        effective_front_vortex_line_strengths = np.zeros(
            self.current_airplane.num_panels
        )
        effective_left_vortex_line_strengths = np.zeros(
            self.current_airplane.num_panels
        )

        # Iterate through the current_airplane's wings.
        for wing in self.current_airplane.wings:

            # Convert this wing's 2D ndarray of panels into a 1D ndarray.
            panels = np.ravel(wing.panels)

            # Iterate through this wing's 1D ndarray panels.
            for panel in panels:

                # Check if this panel is on its wing's right edge.
                if panel.is_right_edge:

                    # Change the effective right vortex line strength from zero to this panel's ring vortex's strength.
                    effective_right_vortex_line_strengths[
                        global_panel_position
                    ] = self.current_vortex_strengths[global_panel_position]

                else:

                    # Get the panel directly to the right of this panel.
                    panel_to_right = wing.panels[
                        panel.local_chordwise_position,
                        panel.local_spanwise_position + 1,
                    ]

                    # Change the effective right vortex line strength from zero to the difference between this panel's
                    # ring vortex's strength, and the ring vortex strength of the panel to the right of it.
                    effective_right_vortex_line_strengths[global_panel_position] = (
                        self.current_vortex_strengths[global_panel_position]
                        - panel_to_right.ring_vortex.strength
                    )

                # Check if this panel is on its wing's leading edge.
                if panel.is_leading_edge:

                    # Change the effective front vortex line strength from zero to this panel's ring vortex's strength.
                    effective_front_vortex_line_strengths[
                        global_panel_position
                    ] = self.current_vortex_strengths[global_panel_position]
                else:

                    # Get the panel directly in front of this panel.
                    panel_to_front = wing.panels[
                        panel.local_chordwise_position - 1,
                        panel.local_spanwise_position,
                    ]

                    # Change the effective front vortex line strength from zero to the difference between this panel's
                    # ring vortex's strength, and the ring vortex strength of the panel in front of it.
                    effective_front_vortex_line_strengths[global_panel_position] = (
                        self.current_vortex_strengths[global_panel_position]
                        - panel_to_front.ring_vortex.strength
                    )

                # Check if this panel is on its wing's left edge.
                if panel.is_left_edge:

                    # Change the effective left vortex line strength from zero to this panel's ring vortex's strength.
                    effective_left_vortex_line_strengths[
                        global_panel_position
                    ] = self.current_vortex_strengths[global_panel_position]
                else:

                    # Get the panel directly to the left of this panel.
                    panel_to_left = wing.panels[
                        panel.local_chordwise_position,
                        panel.local_spanwise_position - 1,
                    ]

                    # Change the effective left vortex line strength from zero to the difference between this panel's
                    # ring vortex's strength, and the ring vortex strength of the panel to the left of it.
                    effective_left_vortex_line_strengths[global_panel_position] = (
                        self.current_vortex_strengths[global_panel_position]
                        - panel_to_left.ring_vortex.strength
                    )

                # Increment the global panel position.
                global_panel_position += 1

        # Calculate the solution velocities at the centers of the panel's front leg, left leg, and right leg.
        velocities_at_ring_vortex_front_leg_centers = (
            self.calculate_solution_velocity(points=self.panel_front_vortex_centers)
            + self.calculate_current_flapping_velocities_at_front_leg_centers()
        )
        velocities_at_ring_vortex_left_leg_centers = (
            self.calculate_solution_velocity(points=self.panel_left_vortex_centers)
            + self.calculate_current_flapping_velocities_at_left_leg_centers()
        )
        velocities_at_ring_vortex_right_leg_centers = (
            self.calculate_solution_velocity(points=self.panel_right_vortex_centers)
            + self.calculate_current_flapping_velocities_at_right_leg_centers()
        )

        # Using the effective line vortex strengths, and the Kutta-Joukowski theorem to find the near field force in
        # geometry axes on the front leg, left leg, and right leg. Also calculate the unsteady component of the
        # force on each panel, which is derived from the unsteady Bernoulli equation.
        near_field_forces_on_ring_vortex_right_legs_geometry_axes = (
            self.current_operating_point.density
            * np.expand_dims(effective_right_vortex_line_strengths, axis=1)
            * np.cross(
                velocities_at_ring_vortex_right_leg_centers,
                self.panel_right_vortex_vectors,
                axis=-1,
            )
        )
        near_field_forces_on_ring_vortex_front_legs_geometry_axes = (
            self.current_operating_point.density
            * np.expand_dims(effective_front_vortex_line_strengths, axis=1)
            * np.cross(
                velocities_at_ring_vortex_front_leg_centers,
                self.panel_front_vortex_vectors,
                axis=-1,
            )
        )
        near_field_forces_on_ring_vortex_left_legs_geometry_axes = (
            self.current_operating_point.density
            * np.expand_dims(effective_left_vortex_line_strengths, axis=1)
            * np.cross(
                velocities_at_ring_vortex_left_leg_centers,
                self.panel_left_vortex_vectors,
                axis=-1,
            )
        )
        unsteady_near_field_forces_geometry_axes = (
            self.current_operating_point.density
            * np.expand_dims(
                (self.current_vortex_strengths - self.last_panel_vortex_strengths),
                axis=1,
            )
            * np.expand_dims(self.panel_areas, axis=1)
            * self.panel_normal_directions
        )

        # Sum the forces on the legs, and the unsteady force, to calculate the total near field force, in geometry
        # axes, on each panel.
        near_field_forces_geometry_axes = (
            near_field_forces_on_ring_vortex_front_legs_geometry_axes
            + near_field_forces_on_ring_vortex_left_legs_geometry_axes
            + near_field_forces_on_ring_vortex_right_legs_geometry_axes
            + unsteady_near_field_forces_geometry_axes
        )

        # Find the near field moment in geometry axes on the front leg, left leg, and right leg. Also find the
        # moment on each panel due to the unsteady force.
        near_field_moments_on_ring_vortex_front_legs_geometry_axes = np.cross(
            self.panel_front_vortex_centers - self.current_airplane.xyz_ref,
            near_field_forces_on_ring_vortex_front_legs_geometry_axes,
            axis=-1,
        )
        near_field_moments_on_ring_vortex_left_legs_geometry_axes = np.cross(
            self.panel_left_vortex_centers - self.current_airplane.xyz_ref,
            near_field_forces_on_ring_vortex_left_legs_geometry_axes,
            axis=-1,
        )
        near_field_moments_on_ring_vortex_right_legs_geometry_axes = np.cross(
            self.panel_right_vortex_centers - self.current_airplane.xyz_ref,
            near_field_forces_on_ring_vortex_right_legs_geometry_axes,
            axis=-1,
        )
        unsteady_near_field_moments_geometry_axes = np.cross(
            self.panel_collocation_points - self.current_airplane.xyz_ref,
            unsteady_near_field_forces_geometry_axes,
            axis=-1,
        )

        # Sum the moments on the legs, and the unsteady moment, to calculate the total near field moment, in
        # geometry axes, on each panel.
        near_field_moments_geometry_axes = (
            near_field_moments_on_ring_vortex_front_legs_geometry_axes
            + near_field_moments_on_ring_vortex_left_legs_geometry_axes
            + near_field_moments_on_ring_vortex_right_legs_geometry_axes
            + unsteady_near_field_moments_geometry_axes
        )

        # Initialize a variable to hold the global panel position.
        global_panel_position = 0

        # Iterate through this solver's panels.
        for panel in self.panels:
            # Update the force and moment on this panel.
            panel.near_field_force_geometry_axes = near_field_forces_geometry_axes[
                global_panel_position, :
            ]
            panel.near_field_moment_geometry_axes = near_field_moments_geometry_axes[
                global_panel_position, :
            ]

            # Update the pressure on this panel.
            panel.update_pressure()

            # Increment the global panel position.
            global_panel_position += 1

            # Sum up the near field forces and moments on every panel to find the total force and moment on the geometry.
        total_near_field_force_geometry_axes = np.sum(
            near_field_forces_geometry_axes, axis=0
        )
        total_near_field_moment_geometry_axes = np.sum(
            near_field_moments_geometry_axes, axis=0
        )

        # Find the total near field force in wind axes from the rotation matrix and the total near field force in
        # geometry axes.
        self.current_airplane.total_near_field_force_wind_axes = (
            np.transpose(
                self.current_operating_point.calculate_rotation_matrix_wind_axes_to_geometry_axes()
            )
            @ total_near_field_force_geometry_axes
        )

        # Find the total near field moment in wind axes from the rotation matrix and the total near field moment in
        # geometry axes.
        self.current_airplane.total_near_field_moment_wind_axes = (
            np.transpose(
                self.current_operating_point.calculate_rotation_matrix_wind_axes_to_geometry_axes()
            )
            @ total_near_field_moment_geometry_axes
        )

        # Calculate the current_airplane's induced drag coefficient
        induced_drag_coefficient = (
            -self.current_airplane.total_near_field_force_wind_axes[0]
            / self.current_operating_point.calculate_dynamic_pressure()
            / self.current_airplane.s_ref
        )

        # Calculate the current_airplane's side force coefficient.
        side_force_coefficient = (
            self.current_airplane.total_near_field_force_wind_axes[1]
            / self.current_operating_point.calculate_dynamic_pressure()
            / self.current_airplane.s_ref
        )

        # Calculate the current_airplane's lift coefficient.
        lift_coefficient = (
            -self.current_airplane.total_near_field_force_wind_axes[2]
            / self.current_operating_point.calculate_dynamic_pressure()
            / self.current_airplane.s_ref
        )

        # Calculate the current_airplane's rolling moment coefficient.
        rolling_moment_coefficient = (
            self.current_airplane.total_near_field_moment_wind_axes[0]
            / self.current_operating_point.calculate_dynamic_pressure()
            / self.current_airplane.s_ref
            / self.current_airplane.b_ref
        )

        # Calculate the current_airplane's pitching moment coefficient.
        pitching_moment_coefficient = (
            self.current_airplane.total_near_field_moment_wind_axes[1]
            / self.current_operating_point.calculate_dynamic_pressure()
            / self.current_airplane.s_ref
            / self.current_airplane.c_ref
        )

        # Calculate the current_airplane's yawing moment coefficient.
        yawing_moment_coefficient = (
            self.current_airplane.total_near_field_moment_wind_axes[2]
            / self.current_operating_point.calculate_dynamic_pressure()
            / self.current_airplane.s_ref
            / self.current_airplane.b_ref
        )

        self.current_airplane.total_near_field_force_coefficients_wind_axes = np.array(
            [induced_drag_coefficient, side_force_coefficient, lift_coefficient]
        )
        self.current_airplane.total_near_field_moment_coefficients_wind_axes = np.array(
            [
                rolling_moment_coefficient,
                pitching_moment_coefficient,
                yawing_moment_coefficient,
            ]
        )

    def calculate_streamlines(self, num_steps=10, delta_time=0.1):
        """Calculates the location of the streamlines coming off the back of the wings.

        :param num_steps: int, optional
            This is the integer number of points along each streamline (not including the initial points). It can be
            increased for higher fidelity visuals. The default value is 10.
        :param delta_time: float, optional
            This is the time in seconds between each time current_step It can be decreased for higher fidelity visuals
            or to make the streamlines shorter. It's default value is 0.1 seconds.
        :return: None
        """

        # Initialize a ndarray to hold this problem's matrix of streamline points.
        self.streamline_points = np.expand_dims(self.seed_points, axis=0)

        # Iterate through the streamline steps.
        for step in range(num_steps):
            # Get the last row of streamline points.
            last_row_streamline_points = self.streamline_points[-1, :, :]

            # Add the freestream velocity to the induced velocity to get the total velocity at each of the last row of
            # streamline points.
            total_velocities = self.calculate_solution_velocity(
                points=last_row_streamline_points
            )

            # Interpolate the positions on a new row of streamline points.
            new_row_streamline_points = (
                last_row_streamline_points + total_velocities * delta_time
            )

            # Stack the new row of streamline points to the bottom of the matrix of streamline points.
            self.streamline_points = np.vstack(
                (
                    self.streamline_points,
                    np.expand_dims(new_row_streamline_points, axis=0),
                )
            )

    def populate_next_airplanes_wake(self, prescribed_wake=True):
        """This method updates the next time step's airplane's wake.

        :param prescribed_wake: Bool, optional
            This parameter determines if the solver uses a prescribed wake model. If false it will use a free-wake,
            which may be more accurate but will make the solver significantly slower. The default is True.

        :return: None
        """

        # Populate the locations of the next airplane's wake's vortex vertices:
        self.populate_next_airplanes_wake_vortex_vertices(
            prescribed_wake=prescribed_wake
        )

        # Populate the locations of the next airplane's wake vortices.
        self.populate_next_airplanes_wake_vortices()

    def populate_next_airplanes_wake_vortex_vertices(self, prescribed_wake=True):
        """This method populates the locations of the next airplane's wake vortex vertices.

        :param prescribed_wake: Bool, optional
            This parameter determines if the solver uses a prescribed wake model. If false it will use a free-wake,
            which may be more accurate but will make the solver significantly slower. The default is True.
        :return: None
        """

        # Check if this is not the last step.
        if self.current_step < self.num_steps - 1:

            # Get the next airplane object and the current airplane's number of wings.
            next_airplane = self.steady_problems[self.current_step + 1].airplane
            num_wings = len(self.current_airplane.wings)

            # Iterate through the wing positions.
            for wing_num in range(num_wings):

                # Get the wing objects at this position from the current and the next airplane.
                this_wing = self.current_airplane.wings[wing_num]
                next_wing = next_airplane.wings[wing_num]

                # Check if this is the first step.
                if self.current_step == 0:

                    # Get the current wing's number of chordwise and spanwise panels.
                    num_spanwise_panels = this_wing.num_spanwise_panels
                    num_chordwise_panels = this_wing.num_chordwise_panels

                    # Set the chordwise position to be at the trailing edge.
                    chordwise_position = num_chordwise_panels - 1

                    # Initialize a matrix to hold the vertices of the new row of wake ring vortices.
                    first_row_of_wake_ring_vortex_vertices = np.zeros(
                        (1, num_spanwise_panels + 1, 3)
                    )

                    # Iterate through the spanwise panel positions.
                    for spanwise_position in range(num_spanwise_panels):

                        # Get the next wing's panel object at this location.
                        next_panel = next_wing.panels[
                            chordwise_position, spanwise_position
                        ]

                        # The position of the next front left wake ring vortex vertex is the next panel's ring vortex's
                        # back left vertex.
                        next_front_left_vertex = next_panel.ring_vortex.back_left_vertex

                        # Add this to the new row of wake ring vortex vertices.
                        first_row_of_wake_ring_vortex_vertices[
                            0, spanwise_position
                        ] = next_front_left_vertex

                        # Check if this panel is on the right edge of the wing.
                        if spanwise_position == (num_spanwise_panels - 1):
                            # The position of the next front right wake ring vortex vertex is the next panel's ring
                            # vortex's back right vertex.
                            next_front_right_vertex = (
                                next_panel.ring_vortex.back_right_vertex
                            )

                            # Add this to the new row of wake ring vortex vertices.
                            first_row_of_wake_ring_vortex_vertices[
                                0, spanwise_position + 1
                            ] = next_front_right_vertex

                    # Set the next wing's matrix of wake ring vortex vertices to a copy of the row of new wake ring
                    # vortex vertices. This is correct because this is the first time step.
                    next_wing.wake_ring_vortex_vertices = np.copy(
                        first_row_of_wake_ring_vortex_vertices
                    )

                    # Initialize variables to hold the number of spanwise vertices.
                    num_spanwise_vertices = num_spanwise_panels + 1

                    # Initialize a new matrix to hold the second row of wake ring vortex vertices.
                    second_row_of_wake_ring_vortex_vertices = np.zeros(
                        (1, num_spanwise_panels + 1, 3)
                    )

                    # Iterate through the spanwise vertex positions.
                    for spanwise_vertex_position in range(num_spanwise_vertices):

                        # Get the corresponding vertex from the first row.
                        wake_ring_vortex_vertex = next_wing.wake_ring_vortex_vertices[
                            0, spanwise_vertex_position
                        ]

                        if prescribed_wake:

                            # If the wake is prescribed, set the velocity at this vertex to the freestream velocity.
                            velocity_at_first_row_wake_ring_vortex_vertex = (
                                self.current_freestream_velocity_geometry_axes
                            )
                        else:

                            # If the wake is not prescribed, set the velocity at this vertex to the solution velocity at
                            # this point.
                            velocity_at_first_row_wake_ring_vortex_vertex = self.calculate_solution_velocity(
                                np.expand_dims(wake_ring_vortex_vertex, axis=0)
                            )

                        # Update the second row with the interpolated position of the first vertex.
                        second_row_of_wake_ring_vortex_vertices[
                            0, spanwise_vertex_position
                        ] = (
                            wake_ring_vortex_vertex
                            + velocity_at_first_row_wake_ring_vortex_vertex
                            * self.delta_time
                        )

                    # Update the wing's wake ring vortex vertex matrix by vertically stacking the second row below it.
                    next_wing.wake_ring_vortex_vertices = np.vstack(
                        (
                            next_wing.wake_ring_vortex_vertices,
                            second_row_of_wake_ring_vortex_vertices,
                        )
                    )

                # If this isn't the first step, then do this.
                else:

                    # Set the next wing's wake ring vortex vertex matrix to a copy of this wing's wake ring vortex
                    # vertex matrix.
                    next_wing.wake_ring_vortex_vertices = np.copy(
                        this_wing.wake_ring_vortex_vertices
                    )

                    # Get the number of chordwise and spanwise vertices.
                    num_chordwise_vertices = next_wing.wake_ring_vortex_vertices.shape[
                        0
                    ]
                    num_spanwise_vertices = next_wing.wake_ring_vortex_vertices.shape[1]

                    # Iterate through the chordwise and spanwise vertex positions.
                    for chordwise_vertex_position in range(num_chordwise_vertices):
                        for spanwise_vertex_position in range(num_spanwise_vertices):

                            # Get the wake ring vortex vertex at this position.
                            wake_ring_vortex_vertex = next_wing.wake_ring_vortex_vertices[
                                chordwise_vertex_position, spanwise_vertex_position
                            ]

                            if prescribed_wake:

                                # If the wake is prescribed, set the velocity at this vertex to the freestream velocity.
                                velocity_at_first_row_wake_vortex_vertex = (
                                    self.current_freestream_velocity_geometry_axes
                                )
                            else:

                                # If the wake is not prescribed, set the velocity at this vertex to the solution
                                # velocity at this point.
                                velocity_at_first_row_wake_vortex_vertex = np.squeeze(
                                    self.calculate_solution_velocity(
                                        np.expand_dims(wake_ring_vortex_vertex, axis=0)
                                    )
                                )

                            # Update the vertex at this point with its interpolated position.
                            next_wing.wake_ring_vortex_vertices[
                                chordwise_vertex_position, spanwise_vertex_position
                            ] += (
                                velocity_at_first_row_wake_vortex_vertex
                                * self.delta_time
                            )

                    # Set the chordwise position to the trailing edge.
                    chordwise_position = this_wing.num_chordwise_panels - 1

                    # Initialize a new matrix to hold the new first row of wake ring vortex vertices.
                    first_row_of_wake_ring_vortex_vertices = np.empty(
                        (1, this_wing.num_spanwise_panels + 1, 3)
                    )

                    # Iterate spanwise through the trailing edge panels.
                    for spanwise_position in range(this_wing.num_spanwise_panels):

                        # Get the panel object at this location on the next airplane's wing object.
                        next_panel = next_wing.panels[
                            chordwise_position, spanwise_position
                        ]

                        # Add the panel object's back left ring vortex vertex to the matrix of new wake ring vortex
                        # vertices.
                        first_row_of_wake_ring_vortex_vertices[
                            0, spanwise_position
                        ] = next_panel.ring_vortex.back_left_vertex

                        if spanwise_position == (this_wing.num_spanwise_panels - 1):
                            # If the panel object is at the right edge of the wing, add its back right ring vortex
                            # vertex to the matrix of new wake ring vortex vertices.
                            first_row_of_wake_ring_vortex_vertices[
                                0, spanwise_position + 1
                            ] = next_panel.ring_vortex.back_right_vertex

                    # Stack the new first row of wake ring vortex vertices above the wing's matrix of wake ring vortex
                    # vertices.
                    next_wing.wake_ring_vortex_vertices = np.vstack(
                        (
                            first_row_of_wake_ring_vortex_vertices,
                            next_wing.wake_ring_vortex_vertices,
                        )
                    )

    def populate_next_airplanes_wake_vortices(self):
        """This method populates the locations of the next airplane's wake vortices.

        :return: None
        """

        # Create a copy of the current airplane.
        current_airplane_copy = copy.deepcopy(self.current_airplane)

        # Check if the current step is not the last step.
        if self.current_step < self.num_steps - 1:

            # Get the next airplane object.
            next_airplane = self.steady_problems[self.current_step + 1].airplane

            # Iterate through the copy of the current airplane's wing positions.
            for wing_num in range(len(current_airplane_copy.wings)):

                # Get the current airplane copy's wing, and the next airplane's wing at this location.
                this_wing_copy = current_airplane_copy.wings[wing_num]
                next_wing = next_airplane.wings[wing_num]

                # Get the next wing's matrix of wake ring vortex vertices.
                next_wing_wake_ring_vortex_vertices = (
                    next_wing.wake_ring_vortex_vertices
                )

                # Get the wake ring vortices from the this wing copy object.
                this_wing_wake_ring_vortices_copy = this_wing_copy.wake_ring_vortices

                # Find the number of chordwise and spanwise vertices in the next wing's matrix of wake ring vortex
                # vertices.
                num_chordwise_vertices = next_wing_wake_ring_vortex_vertices.shape[0]
                num_spanwise_vertices = next_wing_wake_ring_vortex_vertices.shape[1]

                # Initialize a new matrix to hold the new row of wake ring vortices.
                new_row_of_wake_ring_vortices = np.empty(
                    (1, num_spanwise_vertices - 1), dtype=object
                )

                # Stack the new matrix on top of the copy of this wing's matrix and assign it to the next wing.
                next_wing.wake_ring_vortices = np.vstack(
                    (new_row_of_wake_ring_vortices, this_wing_wake_ring_vortices_copy)
                )

                # Iterate through the vertex positions.
                for chordwise_vertex_position in range(num_chordwise_vertices):
                    for spanwise_vertex_position in range(num_spanwise_vertices):

                        # Set booleans to determine if this vertex is on the right and/or trailing edge of the wake.
                        has_right_vertex = (
                            spanwise_vertex_position + 1
                        ) < num_spanwise_vertices
                        has_back_vertex = (
                            chordwise_vertex_position + 1
                        ) < num_chordwise_vertices

                        if has_right_vertex and has_back_vertex:

                            # If this position is not on the right or trailing edge of the wake, get the four vertices
                            # that will be associated with the corresponding ring vortex at this position.
                            front_left_vertex = next_wing_wake_ring_vortex_vertices[
                                chordwise_vertex_position, spanwise_vertex_position
                            ]
                            front_right_vertex = next_wing_wake_ring_vortex_vertices[
                                chordwise_vertex_position, spanwise_vertex_position + 1
                            ]
                            back_left_vertex = next_wing_wake_ring_vortex_vertices[
                                chordwise_vertex_position + 1, spanwise_vertex_position
                            ]
                            back_right_vertex = next_wing_wake_ring_vortex_vertices[
                                chordwise_vertex_position + 1,
                                spanwise_vertex_position + 1,
                            ]

                            if chordwise_vertex_position > 0:
                                # If this is isn't the front of the wake, update the position of the ring vortex at this
                                # location.
                                next_wing.wake_ring_vortices[
                                    chordwise_vertex_position, spanwise_vertex_position
                                ].update_position(
                                    front_left_vertex=front_left_vertex,
                                    front_right_vertex=front_right_vertex,
                                    back_left_vertex=back_left_vertex,
                                    back_right_vertex=back_right_vertex,
                                )

                            if chordwise_vertex_position == 0:
                                # If this is the front of the wake, get the vortex strength from the wing panel's ring
                                # vortex direction in front of it.
                                this_strength_copy = this_wing_copy.panels[
                                    this_wing_copy.num_chordwise_panels - 1,
                                    spanwise_vertex_position,
                                ].ring_vortex.strength

                                # Then, make a new ring vortex at this location, with the panel's ring vortex's
                                # strength, and add it to the matrix of ring vortices.
                                next_wing.wake_ring_vortices[
                                    chordwise_vertex_position, spanwise_vertex_position
                                ] = ps.aerodynamics.RingVortex(
                                    front_left_vertex=front_left_vertex,
                                    front_right_vertex=front_right_vertex,
                                    back_left_vertex=back_left_vertex,
                                    back_right_vertex=back_right_vertex,
                                    strength=this_strength_copy,
                                )

    def calculate_current_flapping_velocities_at_collocation_points(self):
        """ This method gets the velocity due to flapping at all of the current airplane's collocation points.

        :return flapping_velocities: size (M x 3) ndarray of floats, where M is the current airplane's number of panels
            This is an ndarray containing the x, y, and z components of the velocity due to flapping at every one of the
            current airplane's collocation points. Its units are in meters per second. If the current time step is the
            first time step, all the flapping velocities will be zero.
        """

        # Check if the current step is the first step.
        if self.current_step < 1:

            # Set the flapping velocities to be zero for all points. Then, return the flapping velocities.
            flapping_velocities = np.zeros((self.current_airplane.num_panels, 3))
            return flapping_velocities

        # Get the current airplane's collocation points, and the last airplane's collocation points.
        these_collocations = self.panel_collocation_points
        last_collocations = self.last_panel_collocation_points

        # Calculate and return the flapping velocities.
        flapping_velocities = (these_collocations - last_collocations) / self.delta_time
        return flapping_velocities

    def calculate_current_flapping_velocities_at_right_leg_centers(self):
        """ This method gets the velocity due to flapping at the centers of the current airplane's bound ring vortices'
        right legs.

        :return flapping_velocities: size (M x 3) ndarray of floats, where M is the current airplane's number of panels
            This is an ndarray containing the x, y, and z components of the velocity due to flapping at every one of the
            current airplane's bound vortices' right legs' centers. Its units are in meters per second. If the current
            time step is the first time step, all the flapping velocities will be zero.
        """

        # Check if the current step is the first step.
        if self.current_step < 1:

            # Set the flapping velocities to be zero for all points. Then, return the flapping velocities.
            flapping_velocities = np.zeros((self.current_airplane.num_panels, 3))
            return flapping_velocities

        # Get the current airplane's bound vortices' right legs' centers, and the last airplane's bound vortices' right
        # legs' centers.
        these_right_leg_centers = self.panel_right_vortex_centers
        last_right_leg_centers = self.last_panel_right_vortex_centers

        # Calculate and return the flapping velocities.
        flapping_velocities = (
            these_right_leg_centers - last_right_leg_centers
        ) / self.delta_time
        return flapping_velocities

    def calculate_current_flapping_velocities_at_front_leg_centers(self):
        """ This method gets the velocity due to flapping at the centers of the current airplane's bound ring vortices'
        front legs.

        :return flapping_velocities: size (M x 3) ndarray of floats, where M is the current airplane's number of panels
            This is an ndarray containing the x, y, and z components of the velocity due to flapping at every one of the
            current airplane's bound vortices' front legs' centers. Its units are in meters per second. If the current
            time step is the first time step, all the flapping velocities will be zero.
        """

        # Check if the current step is the first step.
        if self.current_step < 1:

            # Set the flapping velocities to be zero for all points. Then, return the flapping velocities.
            flapping_velocities = np.zeros((self.current_airplane.num_panels, 3))
            return flapping_velocities

        # Get the current airplane's bound vortices' front legs' centers, and the last airplane's bound vortices' front
        # legs' centers.
        these_front_leg_centers = self.panel_front_vortex_centers
        last_front_leg_centers = self.last_panel_front_vortex_centers

        # Calculate and return the flapping velocities.
        flapping_velocities = (
            these_front_leg_centers - last_front_leg_centers
        ) / self.delta_time
        return flapping_velocities

    def calculate_current_flapping_velocities_at_left_leg_centers(self):
        """ This method gets the velocity due to flapping at the centers of the current airplane's bound ring vortices'
        left legs.

        :return flapping_velocities: size (M x 3) ndarray of floats, where M is the current airplane's number of panels
            This is an ndarray containing the x, y, and z components of the velocity due to flapping at every one of the
            current airplane's bound vortices' left legs' centers. Its units are in meters per second. If the current
            time step is the first time step, all the flapping velocities will be zero.
        """

        # Check if the current step is the first step.
        if self.current_step < 1:

            # Set the flapping velocities to be zero for all points. Then, return the flapping velocities.
            flapping_velocities = np.zeros((self.current_airplane.num_panels, 3))
            return flapping_velocities

        # Get the current airplane's bound vortices' left legs' centers, and the last airplane's bound vortices' left
        # legs' centers.
        these_left_leg_centers = self.panel_left_vortex_centers
        last_left_leg_centers = self.last_panel_left_vortex_centers

        # Calculate and return the flapping velocities.
        flapping_velocities = (
            these_left_leg_centers - last_left_leg_centers
        ) / self.delta_time
        return flapping_velocities
