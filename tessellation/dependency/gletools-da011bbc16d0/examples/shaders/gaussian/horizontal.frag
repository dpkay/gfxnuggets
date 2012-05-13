uniform sampler2D texture;
uniform vec2 off;

void main(){
    vec2 uv = gl_TexCoord[0].st;
    vec4 a = texture2D(texture, uv) * 0.375;
    vec4 b = texture2D(texture, vec2(uv.x-off.x, uv.y)) * 0.3125;
    vec4 c = texture2D(texture, vec2(uv.x+off.y, uv.y)) * 0.3125;
    gl_FragColor = a+b+c;
}
