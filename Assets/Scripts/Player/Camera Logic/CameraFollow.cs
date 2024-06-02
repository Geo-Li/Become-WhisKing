using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveCamera : MonoBehaviour
{
    public Transform targetPosition;

    void Start()
    {
        // Rotate the camera to face upwards
        transform.rotation = Quaternion.Euler(0, 180, 0);
    }

    // Update is called once per frame
    void Update()
    {
        transform.position = targetPosition.position;
    }
}
