<script lang="ts">
    import { Confetti } from "svelte-confetti";
    import { tick } from "svelte";

    let {
        additional = "",
        additionalTextOnEnable = "",
        enable = async () => {},
        disable = async () => {},
        enabledByDefault = true,
        filledByDefault = false,
        confetti = true,
        rounded = true,
        changeOnClick = true,
    } = $props();
    let isFilled = $state(filledByDefault);

    const interact = (event) => {
        if (!enabledByDefault) return;
        toggleFill();
        if (isFilled) {
            moveConfetti(event);
            enable();
        } else {
            disable();
        }
    };

    const duration = 2000;

    let things = $state([]);
    let timeout;

    let gradient = $state("linear-gradient(45deg, #000000, #000000, #000000)");

    export async function toggleFill() {
        isFilled = !isFilled;

        await tick();

        if (changeOnClick)
            gradient = isFilled
                ? "linear-gradient(45deg, #c979ff, #124aff, #c979ff)"
                : "linear-gradient(45deg, #000000, #000000, #000000)";
    }

    async function moveConfetti(event) {
        const { target, clientX, clientY } = event;

        const elementY = target.getBoundingClientRect().top;
        const elementX = target.getBoundingClientRect().left;

        const x = clientX - elementX;
        const y = clientY - elementY;

        things = [...things, { x, y }];

        clearTimeout(timeout);

        timeout = setTimeout(() => (things = []), duration);
    }
</script>

<div
    class="{!enabledByDefault
        ? 'bg-white/50'
        : 'bg-white'} transition text-nowrap {rounded
        ? 'rounded-lg'
        : ''} px-2 py-1"
    role="button"
    aria-label="Toggle star selection"
    aria-pressed={isFilled ? "true" : "false"}
    class:cursor-pointer={enabledByDefault}
    aria-disabled={!enabledByDefault}
    tabindex={enabledByDefault ? 0 : -1}
    onclick={interact}
    onkeydown={(event) => {
        if (enabledByDefault && event.key === "Enter") {
            interact(event);
        }
    }}
    style="pointer-events: {enabledByDefault ? 'auto' : 'none'}"
>
    <p
        class="gradient-text text transition"
        style="background: {gradient};
        animation: animatedTextGradient 2s ease infinite;
        background-size: 200% auto;
        color: #000;
        background-clip: text;
        -webkit-text-fill-color: transparent;"
    >
        {#if isFilled == true && additionalTextOnEnable !== ""}
            {additionalTextOnEnable}
        {:else}
            {additional}
        {/if}
    </p>
    {#if confetti == true}
        {#each things as thing}
            <div
                class="relative"
                style="left: {thing.x}px; top: {thing.y - 25}px"
            >
                <Confetti fallDistance="20px" amount="10" {duration} />
            </div>
        {/each}
    {/if}
</div>

<style>
    .gradient-text {
        user-select: none; /* Prevent text selection */
        transition: background 5s ease-in-out; /* This makes the gradient transition smooth */
    }

    .text {
        font-weight: 600;
    }

    @keyframes animatedTextGradient {
        to {
            background-position: 200% center;
        }
    }
</style>
