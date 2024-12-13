<script lang="ts">
    import TitledCarousel from "$lib/components/ui/titled-carousel/TitledCarousel.svelte";
    import { bottomGradientSoftness, clamp, redirectTo } from "$lib/utils";

    let {
        backdropUrl = "",
        posterUrl = "",
        posterAlt = "",
        carousel1 = null,
        carousel1Title = "",
        carousel1Basis = 5,
        carousel2 = null,
        carousel2Title = "",
        carousel2Basis = 5,
    } = $props();

    let primaryImageSize = 50;
</script>

<div
    class="z-0 absolute top-0 left-0 w-full h-[{primaryImageSize}vh] bg-cover bg-center bg-no-repeat opacity-55"
    style="height: {primaryImageSize}rem;
               font-family: 'Open Sans';
               background-image: url('{backdropUrl}');"
>
    <div
        class="absolute w-full bg-easing-b-smooth_fade"
        style="bottom: 0rem;
                   height: {bottomGradientSoftness * primaryImageSize}rem;"
    ></div>

    <div
        class="absolute top-0 bg-gradient-to-r from-rich_black to-rich_black/0 w-full"
        style="opacity: 0.9;
                   height: {primaryImageSize}rem;"
    ></div>

    <div
        class="absolute top-0 bg-gradient-to-l from-rich_black to-rich_black/0 w-full"
        style="opacity: 0.9;
                   height: {primaryImageSize}rem;"
    ></div>
</div>
<div
    class="relative flex flex-col mx-auto h-fit drop-shadow-lg pb-8 px-[10vw]"
    style="padding-top: {clamp(primaryImageSize / 2, 0, primaryImageSize)}vh;"
>
    <div class="relative flex flex-row">
        <img
            src={posterUrl}
            class="h-full lg:max-w-[300px] md:max-w-[250px] md:block hidden mr-4"
            alt={posterAlt}
        />
        <slot />
    </div>

    <div class="flex flex-col">
        {#if carousel1 !== null && carousel1.length > 0}
            <TitledCarousel
                title={carousel1Title}
                data={carousel1}
                basis={carousel1Basis}
            ></TitledCarousel>
        {/if}

        {#if carousel2 !== null && carousel2.length > 0}
            <TitledCarousel
                title={carousel2Title}
                data={carousel2}
                basis={carousel2Basis}
            ></TitledCarousel>
        {/if}
    </div>
</div>
