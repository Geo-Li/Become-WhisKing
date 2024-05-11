using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerCamera : MonoBehaviour
{
    //[SerializeField]
    //private float sensX;
    //[SerializeField]
    //private float sensY;

    [SerializeField]
    private float sensitivity;

    [SerializeField]
    private bool isOneDir = false;

    [Header("Camera")]
    [SerializeField]
    private Transform rightEye; // If isOneDir sets to true, understand this as playerCamera
    [SerializeField]
    private Transform leftEye;

    private float xRot;
    private float yRot;

    private Vector2 mouseInput;


    // Start is called before the first frame update
    void Start()
    {
        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;
    }

    // Update is called once per frame
    void Update()
    {
        //float mouseX = Input.GetAxisRaw("Mouse X") * Time.deltaTime * sensX;
        //float mouseY = Input.GetAxisRaw("Mouse Y") * Time.deltaTime * sensY;
        mouseInput = new Vector2(Input.GetAxisRaw("HorizontalCam"), Input.GetAxisRaw("VerticalCam"));
        MoveCamera();
    }

    private void MoveCamera()
    {
        xRot -= mouseInput.y * sensitivity;
        transform.Rotate(0f, mouseInput.x * sensitivity, 0f);
        rightEye.transform.localRotation = Quaternion.Euler(xRot, 0f, 0f);
        if (!isOneDir)
        {
            leftEye.transform.localRotation = Quaternion.Euler(xRot, 0f, 0f);
        }
    }
}
