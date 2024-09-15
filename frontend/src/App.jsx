import { useState, useRef } from "react";
import axios from "axios";

export default function Component() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [after, setAfter] = useState(false);
  const fileUploadRef = useRef(null);
  let test = {};
  const [test2, setTest2] = useState("dscajkbck");

  const handleImageUpload = async (event) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = async (e) => {
        setSelectedImage(e.target?.result);
        setIsLoading(true);

        // Prepare the FormData
        const formData = new FormData();
        formData.append("file", file);

        try {
          // Make the POST request to upload the image using async/await
          const response = await axios.post(
            "http://127.0.0.1:5000/analyze",
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          );

          // Handle the server response, e.g., detection results

          test = response.data;
          test = JSON.stringify(test);
          console.log("asbckcsascjabckjb", test);
          setTest2(test);
          setAfter(true);
        } catch (error) {
          console.error("Error uploading image:", error);
        } finally {
          // Always set loading to false once the process is complete
          setIsLoading(false);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-gray-100">
      <header className="flex items-center justify-between p-4 bg-gray-800">
        <div className="flex items-center space-x-2">
          <h1 className="text-2xl font-bold">DARK DETECT</h1>
        </div>
      </header>

      <main className="flex-grow flex items-center justify-center p-4">
        <div className="max-w-4xl w-full space-y-8">
          <div className="text-center">
            <h2 className="mt-6 text-3xl font-extrabold">Image Detection</h2>
            <p className="mt-2 text-sm text-gray-400">
              Upload an image to detect deceptive and manipulative content
            </p>
          </div>
          <div className="mt-8 space-y-6 flex flex-col md:flex-row md:space-x-8 md:space-y-0">
            <div className="flex-1">
              <div class="flex items-center justify-center w-full">
                <label
                  for="dropzone-file"
                  class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600"
                >
                  <div class="flex flex-col items-center justify-center pt-5 pb-6">
                    <svg
                      class="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 20 16"
                    >
                      <path
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                      />
                    </svg>
                    <p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
                      <span class="font-semibold">Click to upload</span> or drag
                      and drop
                    </p>
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                      SVG, PNG, JPG or GIF (MAX. 800x400px)
                    </p>
                  </div>
                  <input
                    id="dropzone-file"
                    type="file"
                    onChange={handleImageUpload}
                    class="hidden"
                    ref={fileUploadRef}
                  />
                </label>
              </div>
            </div>
            <div className="flex-1">
              <div className="bg-gray-800 p-6 rounded-lg h-full">
                <h3 className="text-xl font-semibold mb-4">
                  Detection Results
                </h3>
                {isLoading ? (
                  <div className="flex items-center justify-center h-32">
                    <span className="w-8 h-8 animate-spin text-purple-500">
                      &#9203; {/* Loader Icon */}
                    </span>
                  </div>
                ) : after > 0 ? (
                  <div>{test2}</div>
                ) : (
                  <p className="text-gray-400">
                    Upload an image to see detection results.{" "}
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-gray-800 text-center p-4">
        <p className="text-sm text-gray-400">
          &copy; 2023 DARK DETECT. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
