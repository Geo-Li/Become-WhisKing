using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

public class Whisking100Pts : MonoBehaviour
{
    public float overallScale = 0.1f;
    public float pointSize = 0.01f;
    public Material color;


    private JArray whiskerPtsData;

    [Header("Whisking Animation")]
    public bool animate = true;
    public int frame = 10;
    public int duration = 3;
    private int totalFrames;
    private float frameDuration;
    private bool forward = true;

    // Start is called before the first frame update
    void Start()
    {
        Dictionary<string, object> rawJsonData = FileLoader.LoadJson("/Users/geo/Desktop/Geo/Projects/Video Game/Become-WhisKing/Python/utils/ratWhiskingArray.json");
        Debug.Log("JSON Loaded Successfully!");
        whiskerPtsData = (JArray)rawJsonData["ratWhiskingArray"];
        // Debug.Log(JsonConvert.SerializeObject(whiskerPtsData, Formatting.Indented));
        // Debug.Log("Whisking Array Length: " + whiskerPtsData.Count);
        // JArray firstPosition = (JArray)whiskerPtsData[0];
        // Debug.Log("First Whisking Length: " + firstPosition.Count);
        // JArray rightAngles = (JArray)firstPosition[0];
        // Debug.Log("Right Angles Length: " + rightAngles.Count);
        // JArray rightData = (JArray)rightAngles[10];
        // Debug.Log(JsonConvert.SerializeObject(rightData, Formatting.Indented));
        // Debug.Log("Right Data Length: " + rightData.Count);

        totalFrames = whiskerPtsData.Count;
        frameDuration = (float)duration / (float)totalFrames;  // should be 51 fps

        // JArray data = GetData(frame, isRight);
        // Display100WhiskerPts(data);
        if (animate)
        {
            StartCoroutine(AnimateWhisking());
        }
        else
        {
            Display100WhiskerPts(GetData(frame, true), true);
            Display100WhiskerPts(GetData(frame, false), false);
        }
    }

    public void UpdateFrame(int numFrames)
    {
        foreach (Transform child in transform) Destroy(child.gameObject);
        // Apply frame rates
        frame = forward ? frame + numFrames : frame - numFrames;
        if (frame >= totalFrames - 1) forward = false;
        if (frame <= 10) forward = true;
    }

    void Update()
    {
        if (frame > 0 && frame < totalFrames && !animate)
        {
            Display100WhiskerPts(GetData(frame, true), true);
            Display100WhiskerPts(GetData(frame, false), false);
        }
    }

    JArray GetData(int frame, bool isRight)
    {
        return (JArray)((JArray)whiskerPtsData[frame])[isRight ? 0 : 1];
    }

    void Display100WhiskerPts(JArray data, bool isRight)
    {
        for (int i = 0; i < data.Count; i++) // should loop 100 times
        {
            JArray xyz = (JArray)data[i];
            JArray xAll = (JArray)xyz[0];
            JArray yAll = (JArray)xyz[1];
            JArray zAll = (JArray)xyz[2];
            for (int j = 0; j < xAll.Count; j++) // should loop 30 times
            {
                float x = (float)xAll[j];
                float y = (float)yAll[j];
                float z = (float)zAll[j];
                // if (i == 0)
                // {
                //     Debug.Log($"The base of the point cloud ({(isRight ? "right" : "left")} whisker {j}): ({x}, {z}, {-y})");
                // }
                // if (i == 99)
                // {
                //     Debug.Log($"The tip of the point cloud ({(isRight ? "right" : "left")} whisker {j}): ({x}, {z}, {-y})");
                // }
                CreateWhiskerVisualization(new Vector3(x, z, y), isRight, i, j);
            }
        }
    }

    void CreateWhiskerVisualization(Vector3 position, bool isRight, int index, int whiskerIndex)
    {
        GameObject sphere = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        sphere.transform.position = position * overallScale; // Scale positions
        sphere.transform.localScale = Vector3.one * pointSize; // Adjust sphere size
        sphere.transform.parent = this.transform; // Set the current GameObject as parent
        sphere.name = "WhiskerPoint_" + frame + "_" +
                    (isRight ? "Right" : "Left") +
                    "_" + whiskerIndex + "_" + index;
        sphere.GetComponent<MeshRenderer>().material = color;
    }

    // Use Gizmos for debugging, which will only render things in the Scene view
    // void OnDrawGizmos()
    // {
    //     Gizmos.color = Color.red;
    //     Gizmos.DrawSphere(new Vector3(0, 0, 0), 0.1f);
    // }

    System.Collections.IEnumerator AnimateWhisking()
    {
        while (true)
        {
            // Debug.Log("Animating Whisking... (frame: " + frame + ")");
            // Destroy previous spheres
            foreach (Transform child in transform) Destroy(child.gameObject); // Remove previous spheres

            // Rotate whiskers
            JArray data;
            bool isRight = true;
            for (int i = 0; i < 2; i++)
            {
                data = GetData(frame, isRight);
                Display100WhiskerPts(data, isRight);
                isRight = false;
            }

            // Apply frame rates
            // frame = (frame + 1) % totalFrames;
            frame = forward ? frame + 1 : frame - 1;
            if (frame >= totalFrames - 1) forward = false;
            if (frame <= 0) forward = true;
            yield return new WaitForSeconds(frameDuration);
        }
    }
}
