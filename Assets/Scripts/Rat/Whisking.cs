using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Globalization;



public class Whisking : MonoBehaviour
{
    private string FILE_PATH = "/Users/geo/Documents/MATLAB/trajectory_data/";

    [SerializeField]
    private float speed = 10.0f; // How fast the whisker swings initially

    private List<Vector3> currAngles = new List<Vector3>(); // Current angle

    // ##########
    private float currentSpeed; // Current speed of oscillation
    private float angleX;
    private bool dirX;
    private float angleY;
    private bool dirY;
    private float angleZ;
    private bool dirZ;
    // private float direction = 1.0f; // Direction of swing
    // ##########

    private float[][] eulerPhisList;
    private float[][] eulerThetasList;
    private float[][] eulerZetasList;

    private float[,] quaternionW;
    private float[,] quaternionX;
    private float[,] quaternionY;
    private float[,] quaternionZ;

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

        // Load the Quaternion angles
        quaternionW = LoadQuaternionAngles(FILE_PATH + "quatw_60fps_1hz.csv");
        quaternionX = LoadQuaternionAngles(FILE_PATH + "quatx_60fps_1hz.csv");
        quaternionY = LoadQuaternionAngles(FILE_PATH + "quaty_60fps_1hz.csv");
        quaternionZ = LoadQuaternionAngles(FILE_PATH + "quatz_60fps_1hz.csv");

        currentSpeed = speed; // Initialize current speed

        for (int i = 0; i < transform.childCount; i++)
        {
            currAngles.Add(transform.GetChild(i).eulerAngles);
        }

        angleX = 0;
        angleY = 45;
        angleZ = 0;
        dirX = true;
        dirY = true;
        dirZ = true;

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
            EulerWhisking(frame);

            // Apply frame rates
            frame = (frame + 1) % totalFrames;
            yield return new WaitForSeconds(frameDuration);
        }
    }

    /// <summary>
    /// Mathf.Deg2Rad
    /// </summary>
    /// <param name="frame"></param>
    void EulerWhisking(int frame)
    {
        // // For X
        // if (angleX < 45 && dirX) {
        //     angleX++;
            
        // }
        // else if (angleX == 0) {
        //     angleX++;
        //     dirX = true;
        // }
        // else if (angleX == 45) {
        //     angleX--;
        //     dirX = false;
        // }
        // else {
        //     angleX--;
        // }
        // // For Y
        // if (angleY < 90 && dirY) {
        //     angleY++;
            
        // }
        // else if (angleY == 45) {
        //     angleY++;
        //     dirY = true;
        // }
        // else if (angleY == 90) {
        //     angleY--;
        //     dirY = false;
        // }
        // else {
        //     angleY--;
        // }
        // // For Z
        // if (angleZ < 45 && dirZ) {
        //     angleZ++;
            
        // }
        // else if (angleZ == 0) {
        //     angleZ++;
        //     dirZ = true;
        // }
        // else if (angleZ == 45) {
        //     angleZ--;
        //     dirZ = false;
        // }
        // else {
        //     angleZ--;
        // }
        // if (angleZ < 45 && dirZ) {
        //     angleZ++;
            
        // }


        // We rotate with left first
        for (int i = 0; i < 27; i++)
        {
            Transform whisker = transform.GetChild(i);
            // Vector3 currAngle = currAngles[i];
            // Quaternion quatAngle = Quaternion.Euler(currAngle);

            float phi = eulerPhisList[i][frame];
            float theta = eulerThetasList[i][frame];
            float zeta = eulerZetasList[i][frame];

            // Quaternion rotation = Quaternion.Euler(180 - theta, -phi, -zeta);
            // whisker.eulerAngles = new Vector3(0, 90, 45);
            // angleX;
            // angleY;
            whisker.localRotation = Quaternion.Euler(-phi, theta, zeta);
        }

        // Then, we rotate with right
        for (int i = 28; i < 55; i++)
        {
            Transform whisker = transform.GetChild(i);
            // Vector3 currAngle = currAngles[i];
            // Quaternion quatAngle = Quaternion.Euler(currAngle);

            float phi = eulerPhisList[i - 28][frame];
            float theta = eulerThetasList[i - 28][frame];
            float zeta = eulerZetasList[i - 28][frame];

            // Quaternion rotation = Quaternion.Euler(theta, -phi, zeta);
            // whisker.eulerAngles = new Vector3(0, -90, -45);
            whisker.localRotation = Quaternion.Euler(-phi, -theta, -zeta);
        }
    }

    void QuaternionWhisking(int frame)
    {
        // We rotate with left first
        for (int i = 0; i < 27; i++)
        {
            Transform whisker = transform.GetChild(i);

            Quaternion rotation = new Quaternion(
                quaternionZ[i + 27, frame],
                quaternionY[i + 27, frame],
                quaternionX[i + 27, frame],
                quaternionW[i + 27, frame]
            );

            whisker.transform.localRotation = rotation;
        }

        // Then, we rotate with right
        for (int i = 28; i < 55; i++)
        {
            Transform whisker = transform.GetChild(i);

            Quaternion rotation = new Quaternion(
                quaternionZ[i - 28, frame],
                quaternionY[i - 28, frame],
                quaternionX[i - 28, frame],
                quaternionW[i - 28, frame]
            );

            whisker.transform.localRotation = rotation;
        }
    }

    private Quaternion EulerToQuaternion(float x, float y, float z, string order)
    {
        Quaternion result = Quaternion.identity;
        foreach (char dimension in order.ToLower()) {
            if (dimension == 'x')
            {
                result *= Quaternion.Euler(x, 0, 0);
            }
            else if (dimension == 'y')
            {
                result *= Quaternion.Euler(0, y, 0);
            }
            else if (dimension == 'z')
            {
                result *= Quaternion.Euler(0, 0, z);
            }
        }
        return result;
    }

    private float[][] LoadEulerAngles(string filePath)
    {
        string[] lines = File.ReadAllLines(filePath);
        float[][] angles = new float[lines.Length][];
        for (int i = 0; i < lines.Length; i++)
        {
            string[] line = lines[i].Split(',');
            angles[i] = new float[line.Length];
            for (int j = 0; j < line.Length; j++)
            {
                angles[i][j] = float.Parse(line[j], CultureInfo.InvariantCulture);
            }
        }
        return angles;
    }

    private float[,] LoadQuaternionAngles(string filePath) {
        string[] lines = File.ReadAllLines(filePath);
        int rows = lines.Length;
        int cols = lines[0].Split(',').Length;
        float[,] angles = new float[rows, cols];

        for (int i = 0; i < rows; i++)
        {
            string[] line = lines[i].Split(',');
            for (int j = 0; j < cols; j++)
            {
                angles[i, j] = float.Parse(line[j]);
            }
        }
        return angles;
    }
}
