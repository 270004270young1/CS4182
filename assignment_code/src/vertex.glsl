#version 330 core

layout(location = 0) in vec3 position;  // Vertex position
layout(location = 1) in vec3 normal;    // Vertex normal

uniform mat4 model;       // Model matrix
uniform mat4 view;        // View matrix
uniform mat4 projection;  // Projection matrix

out vec3 FragPos;         // Interpolated fragment position in world space
out vec3 Normal;          // Interpolated normal vector in world space

void main() {
    // Transform vertex position to world space
    vec4 worldPos = model * vec4(position, 1.0);
    FragPos = vec3(worldPos);

    // Transform normal to world space
    Normal = mat3(transpose(inverse(model))) * normal;

    // Output final clip space position
    gl_Position = projection * view * worldPos;
}
