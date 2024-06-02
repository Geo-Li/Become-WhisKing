using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Globalization;



public class Whisking : MonoBehaviour
{
    private string FILE_PATH = "/Users/geo/Documents/MATLAB/";

    [SerializeField]
    private float maxAngle = 20.0f; // Maximum swing angle from the origin in degrees
    [SerializeField]
    private float speed = 10.0f; // How fast the whisker swings initially

    private List<Vector3> currAngles = new List<Vector3>(); // Current angle

    // ##########
    private float currentSpeed; // Current speed of oscillation
    private float angle;
    private float direction = 1.0f; // Direction of swing
    // ##########

    private float[][] eulerPhisList;
    private float[][] eulerThetasList;
    private float[][] eulerZetasList;

    private int frame;
    private int totalFrames = 60;
    private float frameDuration = 1.0f / 60.0f;  // 60 fps

    void Start()
    {
        // Load the Euler angles
        // The data we have only covers one side of whiskers
        eulerPhisList = LoadEulerAngles(FILE_PATH + "EulerPhisList.csv");
        eulerThetasList = LoadEulerAngles(FILE_PATH + "EulerThetasList.csv");
        eulerZetasList = LoadEulerAngles(FILE_PATH + "EulerZetasList.csv");

        currentSpeed = speed; // Initialize current speed

        for (int i = 0; i < transform.childCount; i++)
        {
            currAngles.Add(transform.GetChild(i).eulerAngles);
        }

        // Start the animation coroutine
        StartCoroutine(AnimateWhisking());
    }

    void Update()
    {
        // // User controls to adjust speed
        // if (Input.GetKeyDown(KeyCode.UpArrow))
        // {
        //     currentSpeed += 1.0f; // Increase the speed
        // }
        // if (Input.GetKeyDown(KeyCode.DownArrow))
        // {
        //     currentSpeed = Mathf.Max(0.0f, currentSpeed - 1.0f); // Decrease the speed, minimum 0
        // }
        // if (Input.GetKeyDown(KeyCode.Space))
        // {
        //     currentSpeed = (currentSpeed == 0.0f) ? speed : 0.0f; // Toggle stop/start
        // }
        // if (Input.GetKeyDown(KeyCode.LeftArrow))
        // {
        //     direction = -1.0f; // Reverse to left
        // }
        // if (Input.GetKeyDown(KeyCode.RightArrow))
        // {
        //     direction = 1.0f; // Reverse to right
        // }

        // // Oscillation logic
        // if (currentSpeed > 0)
        // {
        //     angle += direction * currentSpeed * Time.deltaTime;
        //     if (Mathf.Abs(angle) > maxAngle)
        //     {
        //         angle = Mathf.Sign(angle) * maxAngle;
        //         direction *= -1; // Reverse direction
        //     }

        //     // Apply the rotation to the whisker
        //     RotateWhiskers(angle);
        // }
    }

    System.Collections.IEnumerator AnimateWhisking()
    {
        while (true)
        {
            // Rotate whiskers for both sides
            RotateWhiskers(frame);

            // Apply frame rates
            frame = (frame + 1) % totalFrames;
            yield return new WaitForSeconds(frameDuration);
        }
    }

    /// <summary>
    /// Mathf.Deg2Rad
    /// </summary>
    /// <param name="frame"></param>
    void RotateWhiskers(int frame)
    {
        // We rotate with left first
        for (int i = 0; i < 27; i++)
        {
            Transform whisker = transform.GetChild(i);
            Vector3 currAngle = currAngles[i];
            Quaternion quatAngle = Quaternion.Euler(currAngle);

            float phi = eulerPhisList[i][frame];
            float theta = eulerThetasList[i][frame] - 90;
            float zeta = eulerZetasList[i][frame];

            // Quaternion rotation = Quaternion.Euler(180 - theta, -phi, -zeta);
            Quaternion rotation = Quaternion.Euler(-phi, 180 - theta, zeta);
            whisker.localRotation = rotation;
        }

        // Then, we rotate with right
        for (int i = 28; i < 55; i++)
        {
            Transform whisker = transform.GetChild(i);
            Vector3 currAngle = currAngles[i];
            Quaternion quatAngle = Quaternion.Euler(currAngle);

            float phi = eulerPhisList[i-28][frame];
            float theta = eulerThetasList[i-28][frame] - 90;
            float zeta = eulerZetasList[i-28][frame];

            // Quaternion rotation = Quaternion.Euler(theta, -phi, zeta);
            Quaternion rotation = Quaternion.Euler(-phi, theta, zeta);
            whisker.localRotation = rotation;
            // Let's see if we need to store the currAngle back to the list
            // If the angles are cumulative, then, we don't need to store back
        }

        // for (int i = 0; i < transform.childCount; i++)
        // {
        //     Vector3 currentAngle = currentAngles[i];
        //     Transform child = transform.GetChild(i);
        //     Quaternion quatAngle = Quaternion.Euler(currentAngle);
        //     if (child.name.Contains("R"))
        //     {
        //         // Rotate each child around its local Z-axis
        //         Quaternion angle = Quaternion.Euler(new Vector3(0, 0, deltaAngle));
        //         child.localRotation = quatAngle * angle;
        //     }
        //     else if (child.name.Contains("L"))
        //     {
        //         // Rotate each child around its local Z-axis
        //         Quaternion angle = Quaternion.Euler(new Vector3(0, 0, -deltaAngle));
        //         child.localRotation = quatAngle * angle;
        //     }
        // }
    }

    private float[][] LoadEulerAngles(string filePath)
    {
        string[] lines = File.ReadAllLines(filePath);
        float[][] angles = new float[lines.Length][];
        for (int i = 0; i < lines.Length; i++)
        {
            string[] values = lines[i].Split(',');
            angles[i] = new float[values.Length];
            for (int j = 0; j < values.Length; j++)
            {
                angles[i][j] = float.Parse(values[j], CultureInfo.InvariantCulture);
            }
        }
        return angles;
    }
}
