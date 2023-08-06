#version 120
//precision mediump float;

uniform sampler2D img;
uniform sampler2D coef1234;
uniform sampler2D coef5678;
uniform sampler2D indx1234;
uniform sampler2D indx5678;

varying vec2 pix_inv;

//fragcolor

void main(void) {

  vec2 coord = vec2(gl_FragCoord); //pixel position
  vec2 fcoord = vec2(0.0, 0.0); //to hold 0 to 1.0 image coordinates see pix_inv below
  float ntot = 0.0; //total score of 3x3 grid of pixels
  for (float i=-1.0; i < 2.0; i+=1.0) {
    for (float j=-1.0; j < 2.0; j+=1.0) {
      fcoord = (coord + vec2(i, j)) * pix_inv; // really dividing to scale 0-1 i.e. (x/w, y/h)
      ntot += step(0.25,(texture2D(tex0, fcoord)).b); //add 1.0 if blue > 0.25
    }
  }
  vec4 texc = texture2D(tex0, (coord * pix_inv)); //current value of pixel
  ntot -= step(0.25, texc.b); // take away this square (centre of grid)
  if (ntot == 3.0) texc = vec4(0.0, 0.0, 1.0, 1.0);
  else if (ntot != 2.0) texc = vec4(smoothstep(0.0, 5.0, ntot), 1.0, 0.0, 0.0);
  gl_FragColor = texc;
  gl_FragColor.a = 1.0;
}