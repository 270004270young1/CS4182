#version 330 core

in vec3 FragPos;   // Interpolated fragment position
in vec3 Normal;    // Interpolated normal

out vec4 FragColor;

uniform vec3 lightPos;    // Light position in world space
uniform vec3 viewPos;     // Camera position in world space
uniform vec3 lightColor;  // Light color
uniform vec3 objectColor; // Object color

void main() {
    // Ambient lighting
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * lightColor;

    // Diffuse lighting
    vec3 norm = normalize(Normal);           // Normalize interpolated normal
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    // Specular lighting (Phong model)
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor;

    // Combine lighting components
    vec3 result = (ambient + diffuse + specular) * objectColor;
    FragColor = vec4(result, 1.0);
}
