using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

public class WhiskingOrientations : MonoBehaviour
{
    private JObject whiskingOrientationsData;

    [Header("Whisking Animation")]
    public bool animate = true;
    public int frame = 0;
    public int duration = 3;
    private int totalFrames = 51;
    private float frameDuration;
    private bool forward = true;

    // Start is called before the first frame update
    void Start()
    {
        Dictionary<string, object> rawJsonData = FileLoader.LoadJson("/Users/geo/Desktop/Geo/Projects/Video Game/Become-WhisKing/Python/utils/ratWhiskingOrientations.json");
        Debug.Log("JSON Loaded Successfully!");
        whiskingOrientationsData = (JObject)rawJsonData["ratWhiskingOrientations"];
        // Debug.Log(JsonConvert.SerializeObject(whiskingOrientationsData, Formatting.Indented));
        // JObject rightData = (JObject)whiskingOrientationsData["right"];
        // Debug.Log(JsonConvert.SerializeObject(rightData, Formatting.Indented));
        // JArray rightThetaData = (JArray)rightData["theta"];
        // Debug.Log(JsonConvert.SerializeObject(rightThetaData, Formatting.Indented));
        // JArray whisker10Data = (JArray)rightThetaData[9];
        // Debug.Log(JsonConvert.SerializeObject(whisker10Data, Formatting.Indented));

        // Debug.Log("Total Children: " + transform.childCount);
        frameDuration = (float)duration / (float)totalFrames;  // should be 51 fps

        if (animate)
        {
            StartCoroutine(AnimateWhisking());
        }
    }

    public void UpdateFrame(int numFrames)
    {
        // Apply frame rates
        frame = forward ? frame + numFrames : frame - numFrames;
        if (frame >= totalFrames - 1 - 10) forward = false;
        if (frame <= 0) forward = true;

        // Print out the ends of whiskers
        // foreach (Transform child in transform)
        // {
        //     MeshFilter meshFilter = child.GetComponent<MeshFilter>();
        //     float meshHeight = meshFilter.sharedMesh.bounds.size.y;
        //     Debug.Log($"{child.name} mesh height (world units): {meshHeight}");
        // }
    }

    void Update()
    {
        if (frame > 0 && frame < totalFrames && !animate)
        {
            EulerWhisking(GetData(frame, false), GetData(frame, true));
        }
    }

    Vector3[] GetData(int frame, bool isRight)
    {
        Vector3[] rotations = new Vector3[30];
        JObject data = (JObject)whiskingOrientationsData[isRight ? "right" : "left"];
        JArray thetaData = (JArray)data["theta"];
        JArray phiData = (JArray)data["phi"];
        JArray zetaData = (JArray)data["zeta"];

        for (int i = 0; i < 30; i++)
        {
            JArray whiskerThetaData = (JArray)thetaData[i];
            JArray whiskerPhiData = (JArray)phiData[i];
            JArray whiskerZetaData = (JArray)zetaData[i];

            float theta = (float)whiskerThetaData[frame];
            float phi = (float)whiskerPhiData[frame];
            float zeta = (float)whiskerZetaData[frame];

            rotations[i] = new Vector3(phi, theta, zeta);
        }

        return rotations;
    }

    System.Collections.IEnumerator AnimateWhisking()
    {
        while (true)
        {
            // Debug.Log("Animating Whisking... (frame: " + frame + ")");
            // Rotate whiskers
            EulerWhisking(GetData(frame, false), GetData(frame, true));

            // Apply frame rates
            frame = forward ? frame + 1 : frame - 1;
            if (frame >= totalFrames - 1) forward = false;
            if (frame <= 0) forward = true;
            yield return new WaitForSeconds(frameDuration);
        }
    }

    void EulerWhisking(Vector3[] leftRotations, Vector3[] rightRotations)
    {
        for (int i = 0; i < 16; i++)
        {
            ApplyRotation(i, leftRotations[i], rightRotations[i]);
        }
        for (int i = 16; i < 22; i++)
        {
            ApplyRotation(i, leftRotations[i+1], rightRotations[i+1]);
        }
        for (int i = 22; i < 27; i++)
        {
            ApplyRotation(i, leftRotations[i+2], rightRotations[i+2]);
        }
        // for (int i = 0; i < 27; i++)
        // {
        //     Transform leftWhisker = transform.GetChild(i);
        //     Transform rightWhisker = transform.GetChild(i + 27);
        //     rightWhisker.localRotation = Quaternion.Euler(-leftRotations[i].x, leftRotations[i].y, leftRotations[i].z);
        //     leftWhisker.localRotation = Quaternion.Euler(-rightRotations[i].x, -rightRotations[i].y, -rightRotations[i].z);
        // }
    }

    void ApplyRotation(int index, Vector3 leftRotation, Vector3 rightRotation)
    {
        Transform leftWhisker = transform.GetChild(index);
        Transform rightWhisker = transform.GetChild(index + 27);
        leftWhisker.localRotation = Quaternion.Euler(-leftRotation.x, leftRotation.y, leftRotation.z);
        rightWhisker.localRotation = Quaternion.Euler(-rightRotation.x, -rightRotation.y, -rightRotation.z);
    }
}
