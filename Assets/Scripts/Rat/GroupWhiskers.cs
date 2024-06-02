using System.IO;
using System.Collections.Generic;
using UnityEngine;

public class GroupWhiskers : MonoBehaviour
{

    // [SerializeField]
    // private Transform rat;


    // Start is called before the first frame update
    void Start()
    {
        // Extract whisker names
        string file_path = "/Users/geo/Documents/MATLAB/whiskitphysics/code/data/whisker_param_average_rat/param_name.csv";
        string[] names = File.ReadAllLines(file_path);
        Dictionary<string, Transform> parent = new Dictionary<string, Transform>();

        // Set whiskers as children under rat
        foreach (string whisker_name in names)
        {
            Transform whisker_link1 = transform.Find(whisker_name + "_link1"); // Creating a new parent GameObject
            parent[whisker_name] = whisker_link1;
            // Debug.Log(whisker_name);
        }

        // Iterate through all direct children of the current GameObject
        foreach (Transform child in transform)
        {
            Debug.Log(child.name);
            if (parent.ContainsKey(child.name.Substring(0, 3)))
            {
                Transform link1 = parent[child.name.Substring(0, 3)];
                if (link1 != child)
                {
                    child.SetParent(link1, false);
                }
            }
        }
    }
}
