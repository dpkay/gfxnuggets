#version 410

vertex:
    in vec4 position;
    
    void main(void){
        gl_Position = position;
    }

control:
    layout(vertices = 3) out;
    uniform float inner_level;
    uniform float outer_level;
    #define id gl_InvocationID

    void main(){
        gl_TessLevelInner[0] = inner_level;
        gl_TessLevelOuter[0] = outer_level;
        gl_TessLevelOuter[1] = outer_level;
        gl_TessLevelOuter[2] = outer_level;

        gl_out[id].gl_Position = gl_in[id].gl_Position;
    }

eval:
    layout(triangles, __SPACING, ccw) in;

    uniform mat4 projection;
    uniform mat4 modelview;
    uniform float timestamp;
    uniform float dispStrength;


    float randomizer(const float x)
    {
        float z = mod(x, 5612.0);
        z = mod(z, 3.1415927 * 2.0);
        return(fract(cos(z) * 56812.5453));
    }

    const float A = 1.0;
    const float B = 57.0;
    const float C = 113.0;
    const vec3 ABC = vec3(A, B, C);

    float cnoise(const in vec3 xx)
    {
        vec3 x = mod(xx + 32768.0, 65536.0);
        vec3 ix = floor(x);
        vec3 fx = fract(x);
        vec3 wx = fx*fx*(3.0-2.0*fx);
        float nn = dot(ix, ABC);

        float re = mix(mix(mix(randomizer(nn),
                               randomizer(nn + A),wx.x),
                           mix(randomizer(nn + B),
                               randomizer(nn + A + B),wx.x),wx.y),
                       mix(mix(randomizer(nn + C),
                               randomizer(nn + C + A),wx.x),
                           mix(randomizer(nn + C + B),
                               randomizer(nn + C + B + A),wx.x),wx.y),wx.z);

        return 1.0 - 2.0 * re;
    }

    void main(){
        float u = gl_TessCoord.x;
        float v = gl_TessCoord.y;

        vec4 p = gl_TessCoord.x * gl_in[0].gl_Position + 
                 gl_TessCoord.y * gl_in[1].gl_Position + 
                 gl_TessCoord.z * gl_in[2].gl_Position;
                 
        vec2 noiseCoord = gl_TessCoord.xy*10 + timestamp*vec2(1,0);
        float disp = dispStrength* cnoise(vec3(noiseCoord,0))*0.2;
        p += vec4(0,0,disp,0);

        gl_Position = projection * modelview * p;
    }

geometry:
    layout(triangles) in;
    layout(triangle_strip, max_vertices = 3) out;

    void main(){
        gl_Position = gl_in[0].gl_Position; EmitVertex();
        gl_Position = gl_in[1].gl_Position; EmitVertex();
        gl_Position = gl_in[2].gl_Position; EmitVertex();
        EndPrimitive();
    }

fragment:
    out vec4 fragment;

    void main(){
        fragment = vec4(1.0);
    }
