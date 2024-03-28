using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class movement : MonoBehaviour
{
    [Header("Movement")]
    [SerializeField]
    private float moveSpeed;

    [SerializeField]
    private float jumpForce;

    public Transform orientation;

    private Vector3 moveDir;

    private Rigidbody playerRB;

    // Start is called before the first frame update
    void Start()
    {
        playerRB = GetComponent<Rigidbody>();
        //playerRB.freezeRotation = true;
    }

    // Update is called once per frame
    void Update()
    {
        moveDir = new Vector3(Input.GetAxisRaw("Horizontal"), 0f, Input.GetAxisRaw("Vertical"));
        MovePlayer();
    }

    private void FixedUpdate()
    {
        //moveDir = orientation.forward * verticalInput + orientation.right * horizontalInput;
        //playerRB.AddForce(moveDir.normalized * moveSpeed * 10f, ForceMode.Force);
        //Debug.Log(moveDir);
    }

    private void MovePlayer()
    {
        Vector3 moveVector = transform.TransformDirection(moveDir) * moveSpeed;
        playerRB.velocity = new Vector3(moveVector.x, playerRB.velocity.y, moveVector.z);

        // If jump is needed, uncomment these lines
        if (Input.GetKeyDown(KeyCode.Space))
        {
            playerRB.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
        }
    }
}
