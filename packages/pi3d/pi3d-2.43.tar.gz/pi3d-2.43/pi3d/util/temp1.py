from ctypes import (c_int, byref, Structure, CDLL, POINTER)
from ctypes.util import find_library

egl_name = find_library("EGL")
egl = CDLL(egl_name)

EGL_BUFFER_SIZE = 0x3020
EGL_ALPHA_SIZE = 0x3021
EGL_BLUE_SIZE = 0x3022
EGL_GREEN_SIZE = 0x3023
EGL_RED_SIZE = 0x3024
EGL_DEPTH_SIZE = 0x3025
EGL_STENCIL_SIZE = 0x3026
EGL_SAMPLES = 0x3031
EGL_SURFACE_TYPE = 0x3033
EGL_DEFAULT_DISPLAY = 0

EGLint = c_int

class _EGLDisplay(Structure): ###### EDIT needs this definition to work on gentoo64 is that significant (not needed on laptop 64)
    __slots__ = [
    ]
_EGLDisplay._fields_ = [
    ('_opaque_struct', EGLint)
]
EGLDisplay = POINTER(_EGLDisplay) #######

class _EGLConfig(Structure):
    __slots__ = [
    ]
_EGLConfig._fields_ = [
    ('_opaque_struct', EGLint)
]
EGLConfig = POINTER(_EGLConfig)

egl.eglGetDisplay.restype = EGLDisplay ####### EDIT needs this on gentoo64

display = egl.eglGetDisplay(EGL_DEFAULT_DISPLAY)
r = egl.eglInitialize(display, None, None)
attrib_dict = {EGL_RED_SIZE:"RED_SIZE",
			   EGL_GREEN_SIZE:"GREEN_SIZE",
			   EGL_BLUE_SIZE:"BLUE_SIZE",
			   EGL_DEPTH_SIZE:"DEPTH_SIZE",
			   EGL_ALPHA_SIZE:"ALPHA_SIZE",
			   EGL_BUFFER_SIZE:"BUFFER_SIZE",
			   EGL_SAMPLES:"SAMPLES",
			   EGL_STENCIL_SIZE:"STENCIL_SIZE",
			   EGL_SURFACE_TYPE:"SURFACE_TYPE"}
numconfig = EGLint(0)
poss_configs = (EGLConfig * 50)(*(EGLConfig() for _ in range(50)))
r = egl.eglGetConfigs(display, byref(poss_configs), EGLint(len(poss_configs)), byref(numconfig))
attr_val = EGLint()
for i in range(numconfig.value):
  print(i, "- ", end="")
  for attr in attrib_dict:
    r = egl.eglGetConfigAttrib(display, poss_configs[i], attr, byref(attr_val))
    print("{}={}, ".format(attrib_dict[attr], attr_val.value), end="")
  print("")