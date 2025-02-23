using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ColorWhiskers : MonoBehaviour
{
    public Material red;
    public Material blue;

    // Start is called before the first frame update
    void Start()
    {
        // We rotate with left first
        for (int i = 0; i < 27; i++)
        {
            Transform whisker = transform.GetChild(i);
            ApplyMaterialToChildren(whisker, blue);
        }

        // Then, we rotate with right
        for (int i = 28; i < 55; i++)
        {
            Transform whisker = transform.GetChild(i);
            ApplyMaterialToChildren(whisker, red);
        }
    }

    void ApplyMaterialToChildren(Transform parent, Material mat)
    {
        MeshRenderer meshRenderer = parent.GetComponent<MeshRenderer>();
        if (meshRenderer != null)
        {
            meshRenderer.material = mat;
        }

        // Recursively call this function on all children
        foreach (Transform child in parent)
        {
            ApplyMaterialToChildren(child, mat);
        }
    }
}
