using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ApplyRotation : MonoBehaviour
{
    public Transform obj;
    private float angle;

    // Start is called before the first frame update
    void Start()
    {
        angle = 0;
    }

    // Update is called once per frame
    void Update()
    {
        Quaternion rotation = Quaternion.Euler(angle, 0, 0);
        obj.localRotation = rotation;
        angle += 2;
    }
}
