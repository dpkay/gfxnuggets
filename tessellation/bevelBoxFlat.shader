#version 410

vertex:
    in vec4 position;
    
    void main(void){
        gl_Position = position;
    }

control:
    layout(vertices = 4) out;
    uniform float inner_level;
    uniform float outer_level;
    #define id gl_InvocationID

    void main(){
        gl_TessLevelInner[0] = inner_level;
        gl_TessLevelInner[1] = inner_level;
        gl_TessLevelOuter[0] = outer_level;
        gl_TessLevelOuter[1] = outer_level;
        gl_TessLevelOuter[2] = outer_level;
        gl_TessLevelOuter[3] = outer_level;

        gl_out[id].gl_Position = gl_in[id].gl_Position;
    }

eval:
    layout(quads, __SPACING, ccw) in;

    uniform mat4 projection;
    uniform mat4 modelview;
    out vec3 te_normal; 
    out vec2 te_texcoord;

    void main(){
        float u = gl_TessCoord.x;
        float v = gl_TessCoord.y;

        vec4 a = mix(gl_in[1].gl_Position, gl_in[0].gl_Position, u);
        vec4 b = mix(gl_in[2].gl_Position, gl_in[3].gl_Position, u);
        gl_Position = projection * modelview * mix(a, b, v);

        vec4 i = modelview*gl_in[0].gl_Position;
        vec4 j = modelview*gl_in[1].gl_Position;
        vec4 k = modelview*gl_in[2].gl_Position;
        vec3 ii = i.xyz/i.w;
        vec3 jj = j.xyz/j.w;
        vec3 kk = k.xyz/k.w;
        te_normal = normalize(cross(jj-ii,kk-ii));

        te_texcoord = gl_TessCoord.xy;
    }

geometry:
    layout(triangles) in;
    layout(triangle_strip, max_vertices = 3) out;
    in vec3[3] te_normal;
    in vec2[3] te_texcoord;
    out vec3 geo_normal;
    out vec2 geo_texcoord;

    void main(){
        geo_normal = te_normal[0];
        geo_texcoord = te_texcoord[0];
        gl_Position = gl_in[0].gl_Position;
        EmitVertex();

        geo_normal = te_normal[1];
        geo_texcoord = te_texcoord[1];
        gl_Position = gl_in[1].gl_Position;
        EmitVertex();

        geo_normal = te_normal[2];
        geo_texcoord = te_texcoord[2];
        gl_Position = gl_in[2].gl_Position;
        EmitVertex();
        EndPrimitive();
    }

fragment:
    out vec4 fragment;
    in vec3 geo_normal;
    in vec2 geo_texcoord;

    void main(){
        vec3 Ldir = normalize(vec3(-.3,-.7,-.6));
        vec3 color = vec3(geo_texcoord,0);
        float Kd = dot(normalize(geo_normal),Ldir);
        float Ka = 0.25;
        float K = clamp(Kd+Ka, 0.0, 1.0);
        fragment = vec4(color*K, 1.0);
//          fragment = vec4(-normalize(geo_normal), 1.0);
    }
