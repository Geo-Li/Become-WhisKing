using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ApplyRotation : MonoBehaviour
{
    public Transform obj;

    [Header("Rotation")]
    public string direction = "x";
    public bool isNegative = false;
    [Range(0, 10)] public float speed = 1;
    [Tooltip("The magnitude of the rotation, the rotation will be between -magnitude and +magnitude")]
    [Range(0, 180)] public float magnitude = 45;
    public float xAngle = 15;
    public float yAngle = 30;
    public float zAngle = 45;
    private float angle;

    [Header("Timer")]
    public float duration = 5;
    private float timer;
    private bool isTimerOn = false;

    void Start()
    {
        timer = 0;
        angle = 0;
    }

    void Update()
    {
        // If timer is running, count time and wait
        if (isTimerOn)
        {
            timer += Time.deltaTime;
            if (timer >= duration)
            {
                isTimerOn = false;  // Reset timer
                isNegative = !isNegative;  // Reverse rotation direction
            }
            return; // Prevent further angle updates while waiting
        }

        // angle += isNegative ? -speed : speed;

        // Check if we hit the limits (-magnitude or +magnitude)
        if (Mathf.Abs(angle) >= magnitude)
        {
            angle = Mathf.Clamp(angle, -magnitude, magnitude); // Ensure it stays within limits
            isTimerOn = true;  // Start timer
            timer = 0;  // Reset timer
        }

        // Apply rotation
        Quaternion rotation = direction switch
        {
            "x" => Quaternion.Euler(angle, 0, 0),
            "y" => Quaternion.Euler(0, angle, 0),
            "z" => Quaternion.Euler(0, 0, angle),
            "phi" => Quaternion.Euler(angle, 0, 0),
            "theta" => Quaternion.Euler(0, angle, 0),
            "zeta" => Quaternion.Euler(0, 0, angle),
            "yzx" => Quaternion.Euler(0, yAngle, 0) * Quaternion.Euler(0, 0, zAngle) * Quaternion.Euler(xAngle, 0, 0),
            "yxz" => Quaternion.Euler(0, yAngle, 0) * Quaternion.Euler(xAngle, 0, 0) * Quaternion.Euler(0, 0, zAngle),
            "xzy" => Quaternion.Euler(xAngle, 0, 0) * Quaternion.Euler(0, 0, zAngle) * Quaternion.Euler(0, yAngle, 0),
            "xyz" => Quaternion.Euler(xAngle, 0, 0) * Quaternion.Euler(0, yAngle, 0) * Quaternion.Euler(0, 0, zAngle),
            _ => Quaternion.Euler(xAngle, yAngle, zAngle),
        };

        obj.localRotation = rotation;
    }
}
