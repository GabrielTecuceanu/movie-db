<script lang="ts">
    import * as Carousel from "$lib/components/ui/carousel/index.js";
    import Autoplay from "embla-carousel-autoplay";
    import * as Tooltip from "$lib/components/ui/tooltip";
    import { redirectTo } from "$lib/utils";
    import { onMount } from "svelte";

    let { title = "Carousel Title", data = null, basis = 5 } = $props();

    let windowHeight: number;
    let windowWidth: number = $state();
    const updateWindowSize = () => {
        windowHeight = window.innerHeight;
        windowWidth = window.innerWidth;
    };

    // @ts-ignore
    onMount(async () => {
        updateWindowSize();
        window.addEventListener("resize", updateWindowSize);

        return () => {
            window.removeEventListener("resize", updateWindowSize);
        };
    });
</script>

<div class="relative mt-12 justify-center space-y-3">
    <h1 class="text-4xl" style="font-weight: 700;">{title}</h1>
    <Carousel.Root
        plugins={[
            Autoplay({
                delay: 8000,
                stopOnInteraction: true,
            }),
        ]}
        class="relative mx-auto"
    >
        <Carousel.Content class="-ml-1">
            {#each data as item}
                <Carousel.Item class="pl-1 md:basis-1/3 lg:basis-1/{basis}">
                    {#if item.tooltip !== null && item.redirect !== null}
                        <Tooltip.Root>
                            <Tooltip.Trigger
                                onclick={() => {
                                    redirectTo(`${item.redirect}`);
                                }}
                            >
                                <img
                                    class="transition rounded-lg border-2 border-transparent hover:border-munsell_blue"
                                    src={item.img}
                                    alt={item.alt}
                                />
                            </Tooltip.Trigger>
                            <Tooltip.Content>
                                <p>{item.tooltip}</p>
                            </Tooltip.Content>
                        </Tooltip.Root>
                    {:else}
                        <img
                            class="transition rounded-lg border-2 border-transparent hover:border-munsell_blue"
                            src={item.img}
                            alt={item.alt}
                        />
                    {/if}
                </Carousel.Item>
            {/each}
        </Carousel.Content>
        {#if windowWidth > 550}
            <Carousel.Previous class="bg-transparent" />
            <Carousel.Next class="bg-transparent" />
        {/if}
    </Carousel.Root>
</div>
