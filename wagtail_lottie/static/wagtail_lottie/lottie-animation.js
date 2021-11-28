const lottieElements = document.querySelectorAll('[lottie-animation]')
const isSchemeDark = (window.matchMedia) && (window.matchMedia('(prefers-color-scheme: dark)').matches)
lottieElements.forEach(function (lottieElement) {
    const haveToPlay = (lottieElement.dataset.prefersColorScheme === 'no_scheme')
        || (isSchemeDark && lottieElement.dataset.prefersColorScheme === 'scheme_dark')
        || (!isSchemeDark && lottieElement.dataset.prefersColorScheme === 'scheme_light')
    if (haveToPlay) {
        const animation = bodymovin.loadAnimation({
            container: lottieElement,
            renderer: lottieElement.dataset.renderer,
            loop: lottieElement.dataset.loop === 'True',
            autoplay: lottieElement.dataset.playMode === 'play_auto',
            name: lottieElement.dataset.name,
            path: lottieElement.dataset.json
        })
        if (lottieElement.dataset.playMode === 'play_intersection') {
            const io = new IntersectionObserver(entries => entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animation.play()
                    io.unobserve(lottieElement)
                }
            }))
            io.observe(lottieElement)
        }
    }
})