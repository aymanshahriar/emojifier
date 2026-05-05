import { useState } from 'react'

/** Stand-in base URL until proxy/env is configured */
const API_ORIGIN = 'http://localhost:5000'

function App() {
  const [uploadedImage, setUploadedImage] = useState(null)
  const [emojifiedImage, setEmojifiedImage] = useState(null)
  const [granularity, setGranularity] = useState(250)
  const [isProcessing, setIsProcessing] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')
  const [isDragOver, setIsDragOver] = useState(false)
  const [isDarkMode, setIsDarkMode] = useState(true)

  function setImage(file) {
    if (!file) return
    setUploadedImage(file)
    setEmojifiedImage(null)
    setErrorMessage('')
  }

  function handleImageUpload(e) {
    setImage(e.target.files[0])
  }

  function handleDrop(e) {
    e.preventDefault()
    setIsDragOver(false)
    setImage(e.dataTransfer.files[0])
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (!uploadedImage) return

    const formData = new FormData()
    formData.append('granularity', String(granularity))
    formData.append('image', uploadedImage)

    try {
      setIsProcessing(true)
      setErrorMessage('')
      const res = await fetch(`${API_ORIGIN}/api/emojify`, {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) {
        const errText = await res.text()
        setErrorMessage(errText || `Request failed: ${res.status}`)
        return
      }

      const blob = await res.blob()
      setEmojifiedImage(blob)
    } catch (err) {
      setErrorMessage(err.message || 'Something went wrong. Please try again.')
    } finally {
      setIsProcessing(false)
    }
  }

  function handleDownload() {
    if (!emojifiedImage) return
    const link = document.createElement('a')
    link.href = URL.createObjectURL(emojifiedImage)
    link.download = `emojified_${uploadedImage.name}`
    link.click()
  }

  return (
    <main
      className={`min-h-screen px-4 py-10 transition-colors ${
        isDarkMode ? 'bg-slate-950 text-slate-100' : 'bg-slate-100 text-slate-900'
      }`}
    >
      <section className="mx-auto flex w-full max-w-6xl flex-col gap-8">
        <header className="flex flex-col items-center gap-4 sm:flex-row sm:justify-between">
          <div className="space-y-2 text-center sm:text-left">
            <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">Emojifier</h1>
            <p
              className={`mx-auto max-w-2xl text-sm sm:text-base sm:mx-0 ${
                isDarkMode ? 'text-slate-300' : 'text-slate-600'
              }`}
            >
              Upload an image, set granularity, and convert it into an emoji mosaic.
            </p>
          </div>
          <button
            type="button"
            onClick={() => setIsDarkMode((prev) => !prev)}
            className={`rounded-lg border px-3 py-2 text-sm font-medium transition ${
              isDarkMode
                ? 'border-slate-700 bg-slate-900 text-slate-100 hover:bg-slate-800'
                : 'border-slate-300 bg-white text-slate-700 hover:bg-slate-50'
            }`}
          >
            {isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
          </button>
        </header>

        <div className="grid gap-6 lg:grid-cols-[360px_1fr]">
          <form
            onSubmit={handleSubmit}
            className={`rounded-2xl border p-5 shadow-xl backdrop-blur ${
              isDarkMode
                ? 'border-slate-800 bg-slate-900/70'
                : 'border-slate-200 bg-white/90'
            }`}
          >
            <div className="space-y-5">
              <div className="space-y-2">
                <label
                  htmlFor="image-upload"
                  className={`text-sm font-medium ${isDarkMode ? 'text-slate-200' : 'text-slate-700'}`}
                >
                  Upload image
                </label>
                <label
                  htmlFor="image-upload"
                  onDragOver={(e) => {
                    e.preventDefault()
                    setIsDragOver(true)
                  }}
                  onDragLeave={() => setIsDragOver(false)}
                  onDrop={handleDrop}
                  className={`block cursor-pointer rounded-lg border-2 border-dashed px-4 py-8 text-center text-sm transition ${
                    isDragOver
                      ? 'border-indigo-500 bg-indigo-500/10'
                      : isDarkMode
                        ? 'border-slate-700 bg-slate-950 text-slate-300 hover:border-slate-600'
                        : 'border-slate-300 bg-slate-50 text-slate-600 hover:border-slate-400'
                  }`}
                >
                  <span className="block font-medium">Drag and drop an image</span>
                  <span className="mt-1 block text-xs opacity-80">or click to browse files</span>
                  {uploadedImage && (
                    <span className="mt-3 block truncate text-xs text-indigo-400">{uploadedImage.name}</span>
                  )}
                </label>
                <input type="file" accept="image/*" id="image-upload" onChange={handleImageUpload} className="hidden" />
              </div>

              <div className="space-y-2">
                <label
                  htmlFor="granularity"
                  className={`text-sm font-medium ${isDarkMode ? 'text-slate-200' : 'text-slate-700'}`}
                >
                  Granularity
                </label>
                <p className={`text-xs ${isDarkMode ? 'text-slate-400' : 'text-slate-500'}`}>
                  Number of emojis along the longest side of the output image.
                </p>
                <input
                  type="number"
                  value={granularity}
                  id="granularity"
                  min={1}
                  onChange={(e) => setGranularity(Number(e.target.value))}
                  className={`w-full rounded-lg border px-3 py-2 text-sm outline-none ring-indigo-500 transition focus:ring-2 ${
                    isDarkMode
                      ? 'border-slate-700 bg-slate-950'
                      : 'border-slate-300 bg-white'
                  }`}
                />
              </div>

              <button
                type="submit"
                disabled={!uploadedImage || isProcessing}
                className="w-full rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-slate-700"
              >
                {isProcessing ? 'Processing...' : 'Emojify'}
              </button>

              {emojifiedImage && (
                <button
                  type="button"
                  onClick={handleDownload}
                  className={`w-full rounded-lg border px-4 py-2.5 text-sm font-medium transition ${
                    isDarkMode
                      ? 'border-emerald-400/50 bg-emerald-500/15 text-emerald-200 hover:bg-emerald-500/25'
                      : 'border-emerald-300 bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
                  }`}
                >
                  Download emojified image
                </button>
              )}

              {errorMessage && (
                <div
                  className={`rounded-lg border px-4 py-3 text-sm ${
                    isDarkMode
                      ? 'border-rose-500/40 bg-rose-500/15 text-rose-200'
                      : 'border-rose-300 bg-rose-50 text-rose-700'
                  }`}
                >
                  {errorMessage}
                </div>
              )}
            </div>
          </form>

          <section className="grid gap-6 md:grid-cols-2">
            <article
              className={`overflow-hidden rounded-2xl border p-4 shadow-xl ${
                isDarkMode
                  ? 'border-slate-800 bg-slate-900/70'
                  : 'border-slate-200 bg-white/90'
              }`}
            >
              <h2 className={`mb-3 text-sm font-semibold uppercase tracking-wide ${isDarkMode ? 'text-slate-300' : 'text-slate-500'}`}>
                Original
              </h2>
              {uploadedImage ? (
                <img
                  src={URL.createObjectURL(uploadedImage)}
                  alt="Uploaded image"
                  className={`h-[420px] w-full rounded-xl object-contain ${isDarkMode ? 'bg-slate-950' : 'bg-slate-100'}`}
                />
              ) : (
                <div
                  className={`flex h-[420px] items-center justify-center rounded-xl text-sm ${
                    isDarkMode ? 'bg-slate-950 text-slate-500' : 'bg-slate-100 text-slate-400'
                  }`}
                >
                  Upload an image to preview it here.
                </div>
              )}
            </article>

            <article
              className={`overflow-hidden rounded-2xl border p-4 shadow-xl ${
                isDarkMode
                  ? 'border-slate-800 bg-slate-900/70'
                  : 'border-slate-200 bg-white/90'
              }`}
            >
              <h2 className={`mb-3 text-sm font-semibold uppercase tracking-wide ${isDarkMode ? 'text-slate-300' : 'text-slate-500'}`}>
                Emojified
              </h2>
              {emojifiedImage ? (
                <img
                  src={URL.createObjectURL(emojifiedImage)}
                  alt="Emojified image"
                  className={`h-[420px] w-full rounded-xl object-contain ${isDarkMode ? 'bg-slate-950' : 'bg-slate-100'}`}
                />
              ) : (
                <div
                  className={`flex h-[420px] items-center justify-center rounded-xl text-sm ${
                    isDarkMode ? 'bg-slate-950 text-slate-500' : 'bg-slate-100 text-slate-400'
                  }`}
                >
                  {isProcessing ? 'Generating emoji mosaic...' : 'Your generated emoji mosaic will appear here.'}
                </div>
              )}
            </article>
          </section>
        </div>

      </section>
    </main>
  )
}

export default App
