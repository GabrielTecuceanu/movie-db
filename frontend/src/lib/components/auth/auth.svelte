<script lang="ts">
    import { onMount } from "svelte";
    import { Icons } from "$lib/components/icons/index.js";
    import { Button, buttonVariants } from "$lib/components/ui/button/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { apiKey } from "$lib/utils";

    import Cookies from "js-cookie";

    let className: string | undefined | null = undefined;
    export { className as class };

    let email = $state("");
    let username = $state("");
    let password = $state("");
    let confirmPassword = $state("");
    let isLoading = $state(false);
    let error = $state("");

    function reset() {
        email = "";
        username = "";
        password = "";
        confirmPassword = "";
    }

    async function onSubmit(event) {
        event.preventDefault();
        isLoading = true;

        const formData = {
            email,
            ...(authState && { username }), // Include username if authState is true (signup)
            password,
            ...(authState && { confirmPassword }), // Include confirmPassword if authState is true
        };

        try {
            const url = authState
                ? `${apiKey}/register` // Replace with your signup endpoint
                : `${apiKey}/login`; // Replace with your login endpoint

            let response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                error = errorData.error;
                throw new Error(
                    `Could not ${authState ? "sign up" : "log in"}.`,
                );
            }

            let result = await response.json();
            if (authState == false) {
                let loginData = { email, password };
                const loginResponse = await fetch(`${apiKey}/login`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(loginData),
                });
                if (!response.ok) {
                    throw new Error(
                        `Could not ${authState ? "sign up" : "log in"}.`,
                    );
                }

                result = await loginResponse.json();
            }
            Cookies.set("token", result.token, { expires: 7 });
            window.location.reload();
        } catch (error) {
            console.error("Error:", error);
        } finally {
            isLoading = false; // Reset loading state
        }
    }

    let { cancel = () => {} } = $props();
    let auth = $state(null);
    let authState = $state(false);

    export function open() {
        setTimeout(() => {
            document.addEventListener("click", clickOutside);
        }, 100);
    }

    export function close() {
        error = "";
        reset();
        document.removeEventListener("click", clickOutside);
        cancel();
    }

    export function setLogin() {
        reset();
        authState = false;
    }

    export function setSignUp() {
        reset();
        authState = true;
    }

    function clickOutside(event) {
        if (auth && !auth.contains(event.target)) close();
    }

    onMount(() => {
        return () => {};
    });
</script>

<div
    class="fixed top-0 left-0 h-screen w-screen bg-black/75 backdrop-blur-sm
           flex items-center justify-center"
    style="font-family: 'Open Sans'; font-weight: 600;"
>
    <div
        bind:this={auth}
        class="bg-rich_black/90 flex flex-row drop-shadow-xl py-8 border-[2px] border-white/20
               lg:w-[400px] md:w-[400px] sm:w-[400px]
               h-fit m-auto rounded-md scale-[1]"
    >
        <div class="flex-1 px-8">
            <div class="flex flex-col space-y-4 text-center">
                <h1 class="text-2xl font-semibold tracking-tight">
                    {#if authState}
                        Create an account
                    {:else}
                        Log in
                    {/if}
                </h1>
                <p class="text-muted-foreground text-sm">
                    {#if authState}
                        Enter your email below to create your account.
                    {:else}
                        Enter your email and password below to log in.
                    {/if}
                </p>

                <div class="grid gap-6">
                    <form onsubmit={onSubmit}>
                        <div class="grid space-y-16">
                            <div class="grid gap-1">
                                {#if authState}
                                    <Label class="sr-only" for="email"
                                        >Email</Label
                                    >
                                    <Input
                                        placeholder="name@example.com"
                                        type="email"
                                        autocapitalize="none"
                                        autocomplete="email"
                                        autocorrect="off"
                                        disabled={isLoading}
                                        bind:value={email}
                                    />
                                    <Label class="sr-only" for="Username"
                                        >Username</Label
                                    >
                                    <Input
                                        placeholder="Username"
                                        type="text"
                                        autocomplete="username"
                                        autocapitalize="none"
                                        autocorrect="off"
                                        disabled={isLoading}
                                        bind:value={username}
                                    />
                                    <Label class="sr-only" for="password"
                                        >Password</Label
                                    >
                                    <Input
                                        placeholder="Password"
                                        type="password"
                                        autocomplete="new-password"
                                        autocapitalize="none"
                                        autocorrect="off"
                                        disabled={isLoading}
                                        bind:value={password}
                                    />
                                    <Label class="sr-only" for="password"
                                        >Confirm password</Label
                                    >
                                    <Input
                                        placeholder="Confirm password"
                                        type="password"
                                        autocomplete="current-password"
                                        autocapitalize="none"
                                        autocorrect="off"
                                        disabled={isLoading}
                                        bind:value={confirmPassword}
                                    />
                                {:else}
                                    <Label class="sr-only" for="email"
                                        >Email</Label
                                    >
                                    <Input
                                        placeholder="name@example.com"
                                        type="email"
                                        autocapitalize="none"
                                        autocomplete="email"
                                        autocorrect="off"
                                        disabled={isLoading}
                                        bind:value={email}
                                    />
                                    <Label class="sr-only" for="password"
                                        >Password</Label
                                    >
                                    <Input
                                        placeholder="Password"
                                        type="password"
                                        autocomplete="new-password"
                                        autocapitalize="none"
                                        autocorrect="off"
                                        disabled={isLoading}
                                        bind:value={password}
                                    />
                                {/if}
                            </div>
                            <Button
                                type="submit"
                                disabled={isLoading}
                                class="bg-white text-rich_black hover:text-rich_black hover:bg-white"
                            >
                                {#if isLoading}
                                    <Icons.spinner
                                        class="mr-2 h-4 w-4 animate-spin"
                                    />
                                {/if}
                                {#if authState}
                                    Create account
                                {:else}
                                    Log in
                                {/if}
                            </Button>
                        </div>
                    </form>
                </div>

                {#if confirmPassword !== "" && password != "" && confirmPassword !== password}
                    <p class="text-red-500" style="font-weight = 400;">
                        Passwords do not match!
                    </p>
                {/if}

                {#if error !== null && error !== ""}
                    <p class="text-red-500" style="font-weight = 400;">
                        Error: {error}
                    </p>
                {/if}

                <p class="text-muted-foreground px-8 text-center text-sm">
                    {#if authState}
                        Already have an account?
                    {:else}
                        New around here?
                    {/if}
                    <!-- svelte-ignore a11y_invalid_attribute -->
                    <a
                        href="javascript:void(0);"
                        class="hover:text-white underline underline-offset-4"
                        onclick={() => {
                            if (authState == false) {
                                setSignUp();
                            } else {
                                setLogin();
                            }
                        }}
                    >
                        {#if authState}
                            Log in here
                        {:else}
                            Sign up
                        {/if}
                    </a>.
                </p>
            </div>
        </div>
    </div>
</div>
