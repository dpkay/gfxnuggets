#version 410

vertex:
    in vec4 position;
    
    void main(void){
        gl_Position = position;
    }

control:
    layout(vertices = 6) out;
    uniform float inner_level;
    uniform float outer_level;
    #define id gl_InvocationID

    void main(){
        gl_TessLevelInner[0] = inner_level;
        gl_TessLevelInner[1] = 0;
        gl_TessLevelOuter[0] = 1;
        gl_TessLevelOuter[1] = outer_level;
        gl_TessLevelOuter[2] = 1;
        gl_TessLevelOuter[3] = outer_level;

        gl_out[id].gl_Position = gl_in[id].gl_Position;
    }

eval:
    layout(quads, __SPACING, ccw) in;

    uniform mat4 projection;
    uniform mat4 modelview;

    out vec3 te_normal;

    void main(){
        float u = gl_TessCoord.x;
        float v = gl_TessCoord.y;
        vec4 a = (1-u)*(1-u)*gl_in[1].gl_Position + 2*(1-u)*u*gl_in[0].gl_Position + u*u*gl_in[5].gl_Position;
        vec4 b = (1-u)*(1-u)*gl_in[2].gl_Position + 2*(1-u)*u*gl_in[3].gl_Position + u*u*gl_in[4].gl_Position;
        gl_Position = projection * modelview * mix(a, b, v);

//        vec4 da_du = 2*(u-1)*gl_in[1].gl_Position + 

//         te_normal = 
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
