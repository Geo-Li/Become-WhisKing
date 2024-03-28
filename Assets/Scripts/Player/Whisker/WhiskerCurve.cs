using System.Collections;
using System.Collections.Generic;
using UnityEngine;


[RequireComponent(typeof(LineRenderer))]
public class WhiskerCurve : MonoBehaviour
{
    [SerializeField]
    private Transform startPoint;
    [SerializeField]
    private Transform endPoint;
    [SerializeField]
    private List<Vector3> controlPoints;



    [SerializeField]
    private int num_seg = 12;




    private LineRenderer lineRenderer;

    // Start is called before the first frame update
    void Start()
    {
        lineRenderer = GetComponent<LineRenderer>();

    }


    void WhiskerGenerator()
    {
        lineRenderer.positionCount = num_seg;
        for (int i=0; i<num_seg; i++)
        {
            float t = i / (float)(num_seg - 1);
            Vector3 position = CalculateBezierPoint(t, controlPoints);
            lineRenderer.SetPosition(i, position);
        }
    }


    Vector3 CalculateBezierPoint(float t, List<Vector3> controlPoints)
    {
        float u = 1 - t;
        Vector3 point = Mathf.Pow(u, 4) * controlPoints[0]; // the first term
        point += 4 * Mathf.Pow(u, 3) * t * controlPoints[1]; // the second term
        point += 6 * Mathf.Pow(u, 2) * Mathf.Pow(t, 2) * controlPoints[2]; // the third term
        point += 4 * u * Mathf.Pow(t, 3) * controlPoints[3]; // the fourth term
        point += Mathf.Pow(t, 4) * controlPoints[4];

        return point;
    }


    // Update is called once per frame
    void Update()
    {
        // whisk when the button is pressed
    }
}
