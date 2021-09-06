# School Timetabling with GA

The objective of this work is to evaluate a genetic
algorithm that uses an direct representation to solve the school
timetabling problem. The problem is designed as a multiobjective
optimization with constraints.

---

## Introduction

The school timetabling problem is a common problem faced by many schools. It is a combinatorial NP-hard problem where the main goal is to allocate teachers in the slots of
the week timetable and at the classes they are assigned to. In
most schools, timetables are manually designed and require
a significant time to be computed with results that often do
not satisfy all the requirements. These requirements may be
structural (like clashes), imposed by the law or tailored for
the specific school we are working with. For example some
teachers may teach in different schools and have only few
days available that have to be considered when creating our
timetable.

The requirements are designed as hard and soft constraints that need to be solved, minimizing the fitness function. An ad-hoc method to generate good initial individuals is described, together with specific
genetic operators. Different tests are performed to evaluate the performance of the algorithm and the results are shown.
