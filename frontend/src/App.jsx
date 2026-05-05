import { useState } from 'react'

/** Stand-in base URL until proxy/env is configured */
const API_ORIGIN = 'http://localhost:5000'

function App() {
  const [uploadedImage, setUploadedImage] = useState(null)
  const [emojifiedImage, setEmojifiedImage] = useState(null)
  const [granularity, setGranularity] = useState(250)
  
  function handleImageUpload(e) {
    const file = e.target.files[0]
    if (file) {
      setUploadedImage(file)
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (!uploadedImage) return

    const formData = new FormData()
    formData.append('granularity', String(granularity))
    formData.append('image', uploadedImage)

    try {
      const res = await fetch(`${API_ORIGIN}/api/emojify`, {
        method: 'POST',
        body: formData,
      })
      console.log(res)
      if (!res.ok) {
        const errText = await res.text()
        console.error(errText || `Request failed: ${res.status}`)
        return
      }

      const blob = await res.blob()
      setEmojifiedImage(blob)
    } catch (err) {
      console.error(err)
    }
  }

  function handleDownload() {
    const link = document.createElement('a')
    link.href = URL.createObjectURL(emojifiedImage)
    link.download = `emojified_${uploadedImage.name}`
    link.click()
  }


  
  return (
    <main className="app-shell">
      <h1>Emojifier</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor='image-upload'>Upload Image</label>
        <input type='file' accept='image/*' id='image-upload' onChange={handleImageUpload} />
        
        <label htmlFor='granularity'>Granularity (number of emojis in the longer side of the image)</label>
        <input type='number' defaultValue={250} id='granularity' min={1} 
        onChange={e => setGranularity(e.target.value)}/>

        {uploadedImage && <button type='submit'>Emojify!</button>}

      </form>
      {uploadedImage && <img src={URL.createObjectURL(uploadedImage)} alt='Uploaded image' />}
      {emojifiedImage && <img src={URL.createObjectURL(emojifiedImage)} alt='Emojified image' />}
      {emojifiedImage && <button onClick={handleDownload}>Download</button>}
    </main>
  )
}

export default App
