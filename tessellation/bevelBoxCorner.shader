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
        gl_TessLevelOuter[0] = outer_level;
        gl_TessLevelOuter[1] = outer_level;
        gl_TessLevelOuter[2] = outer_level;

        gl_out[id].gl_Position = gl_in[id].gl_Position;
    }

eval:
    layout(triangles, __SPACING, ccw) in;

    uniform mat4 projection;
    uniform mat4 modelview;

    void main(){
        float u = gl_TessCoord.x;
        float v = gl_TessCoord.y;
        float w = gl_TessCoord.z;

        vec4 p = u*u*gl_in[1].gl_Position + 
                 v*v*gl_in[3].gl_Position + 
                 w*w*gl_in[5].gl_Position +
                 2*u*v*gl_in[2].gl_Position + 
                 2*v*w*gl_in[4].gl_Position + 
                 2*w*u*gl_in[0].gl_Position;


                 
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
