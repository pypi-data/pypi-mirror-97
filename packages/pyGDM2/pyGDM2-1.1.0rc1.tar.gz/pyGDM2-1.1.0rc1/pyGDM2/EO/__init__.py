"""
pyGDM2.EO - evolutionary optimization toolkit for use with pyGDM2. 


    Copyright (C) 2017-2021, P. R. Wiecha

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    


Additional requirements :
    - pyGMO2/paGMO2 (https://esa.github.io/pagmo2/)


"""
__name__ = 'pyGDM2 - EO'
__author__ = 'Peter R. Wiecha'

__all__ = ["EO.core", "EO.models", "EO.problems", "EO.tools"]

## make modules available
import pyGDM2.EO.core
import pyGDM2.EO.models
import pyGDM2.EO.problems
import pyGDM2.EO.tools
