<script lang="ts">
    import {
        apiKey,
        redirectTo,
        imgBaseUrl,
        imgOriginal,
        fetchUser,
        friendStatus,
    } from "$lib/utils";
    import Cookies from "js-cookie";
    import { onMount } from "svelte";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index";
    import { Separator } from "$lib/components/ui/separator";
    import { page } from "$app/stores";
    import Button from "$lib/components/ui/button/button.svelte";
    import * as Tabs from "$lib/components/ui/tabs";
    import { Input } from "$lib/components/ui/input";
    import * as Card from "$lib/components/ui/card/index";
    import { Label } from "$lib/components/ui/label";

    const username = $page.params.username;
    let loading = $state(true);
    let user = $state(null);
    let friends = $state(null);
    let addFrientText = $state("Add friend");
    const content = [];

    async function fetchProfile() {
        try {
            let response = await fetch(
                `${apiKey}/get_user/username/${username}`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                },
            );
            if (!response.ok) {
                throw new Error(`Could not get profile: ${response.status}`);
            }

            let data = await response.json();

            data.movie_finished = await Promise.all(
                data.movie_finished.map(async (elem) => {
                    let response = await fetch(
                        `${apiKey}/movie/details/${elem.movie_id}`,
                    );
                    if (!response.ok) {
                        throw new Error(
                            `Could not get movie details: ${response.status}`,
                        );
                    }
                    const data = await response.json();
                    return {
                        ...elem,
                        data,
                        poster: `${imgBaseUrl}/${imgOriginal}${data.poster_path}`,
                    };
                }),
            );
            content.push({
                tab_name: "Finished Movies",
                tab_value: "FinishedMovies",
                description: "Revisit your finished movies here",
                media_type: "movie",
                data: data.movie_finished,
            });

            data.movie_watchlist = await Promise.all(
                data.movie_watchlist.map(async (elem) => {
                    let response = await fetch(
                        `${apiKey}/movie/details/${elem}`,
                    );
                    if (!response.ok) {
                        throw new Error(
                            `Could not get movie details: ${response.status}`,
                        );
                    }
                    const data = await response.json();
                    return {
                        ...elem,
                        data,
                        poster: `${imgBaseUrl}/${imgOriginal}${data.poster_path}`,
                    };
                }),
            );
            content.push({
                tab_name: "Movie Watchlist",
                tab_value: "MovieWatchlist",
                description: "Pick your next movie",
                media_type: "movie",
                data: data.movie_watchlist,
            });

            data.tv_finished = await Promise.all(
                data.tv_finished.map(async (elem) => {
                    let response = await fetch(
                        `${apiKey}/tv/details/${elem.show_id}`,
                    );
                    if (!response.ok) {
                        throw new Error(
                            `Could not get show details: ${response.status}`,
                        );
                    }
                    const data = await response.json();
                    return {
                        ...elem,
                        data,
                        poster: `${imgBaseUrl}/${imgOriginal}${data.poster_path}`,
                    };
                }),
            );
            content.push({
                tab_name: "Finished TV Shows",
                tab_value: "FinishedTV",
                description: "Binge-rewatch a show",
                media_type: "tv",
                data: data.tv_finished,
            });

            data.tv_watchlist = await Promise.all(
                data.tv_watchlist.map(async (elem) => {
                    let response = await fetch(`${apiKey}/tv/details/${elem}`);
                    if (!response.ok) {
                        throw new Error(
                            `Could not get show details: ${response.status}`,
                        );
                    }
                    const data = await response.json();
                    return {
                        ...elem,
                        data,
                        poster: `${imgBaseUrl}/${imgOriginal}${data.poster_path}`,
                    };
                }),
            );
            content.push({
                tab_name: "TV Show Watchlist",
                tab_value: "TVWatchlist",
                description: "Pick your next TV show",
                media_type: "tv",
                data: data.tv_watchlist,
            });

            data.favourite_people = await Promise.all(
                data.favourite_people.map(async (elem) => {
                    let response = await fetch(
                        `${apiKey}/person/details/${elem}`,
                    );
                    if (!response.ok) {
                        throw new Error(
                            `Could not get person details: ${response.status}`,
                        );
                    }
                    const data = await response.json();
                    return {
                        ...elem,
                        data,
                        poster: `${imgBaseUrl}/${imgOriginal}${data.profile_path}`,
                    };
                }),
            );
            content.push({
                tab_name: "Followed people",
                tab_value: "FollowedPeople",
                description: "These are the people you follow",
                media_type: "person",
                data: data.favourite_people,
            });

            data.feed = data.feed.reverse();

            return data;
        } catch (e) {
            console.error(e);
        }
    }

    async function fetchFriends() {
        let response = await fetch(`${apiKey}/friends/get_friends`, {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });
        if (!response.ok) {
            throw new Error(`Could not get friends: ${response.status}`);
        }

        let friendsData = await response.json();
        console.log(friendsData);
        friendsData = await Promise.all(
            friendsData.map(async (req) => {
                let response = await fetch(
                    `${apiKey}/get_user/email/${user.email === req.sender ? req.recipient : req.sender}`,
                );
                if (!response.ok) {
                    throw new Error(
                        `Could not get user details: ${response.status}`,
                    );
                }
                const data = await response.json();
                return { username: data.username, since: req.since };
            }),
        );
        return friendsData;
    }

    async function fetchFriendRequests() {
        try {
            let response = await fetch(
                `${apiKey}/friends/get_pending_requests`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                },
            );
            if (!response.ok) {
                throw new Error(
                    `Could not get pending requests: ${response.status}`,
                );
            }

            let data = await response.json();
            data = await Promise.all(
                data.map(async (req) => {
                    let response = await fetch(
                        `${apiKey}/get_user/email/${req.sender}`,
                        {
                            method: "GET",
                            headers: {
                                "Content-Type": "application/json",
                            },
                        },
                    );
                    if (!response.ok) {
                        throw new Error(
                            `Could not get sender: ${response.status}`,
                        );
                    }

                    let data = await response.json();
                    return { ...req, username: data.username };
                }),
            );
            return data;
        } catch (e) {
            console.error(e);
        }
    }

    let reqs = $state(null);
    let isLoggedIn = $state(false);
    let loggedUser = $state(null);
    const token = Cookies.get("token");
    if (token) isLoggedIn = true;
    let isFriend: friendStatus = $state(friendStatus.STRANGER);

    // @ts-ignore
    onMount(async () => {
        user = await fetchProfile();

        if (isLoggedIn) {
            loggedUser = await fetchUser(token);
            if (loggedUser.username === username) {
                isFriend = friendStatus.ME;
            } else {
                try {
                    let response = await fetch(`${apiKey}/friends/is_friend`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                        },
                        body: JSON.stringify({
                            email: user.email,
                        }),
                    });

                    const data = await response.json();
                    if (data.status === true) isFriend = friendStatus.FRIEND;
                } catch (e) {
                    console.error(e);
                }
            }
            if (isFriend === friendStatus.ME) {
                reqs = await fetchFriendRequests();
            }

            friends = await fetchFriends();
        }

        loading = false;

        return () => {};
    });
</script>

{#if user !== null && !loading}
    <Tabs.Root value="account" class="w-fit mt-16 min-h-screen mx-auto">
        <Tabs.List class="grid w-full grid-cols-8">
            <Tabs.Trigger value="account">Account</Tabs.Trigger>
            {#if isFriend === friendStatus.ME}
                <Tabs.Trigger value="feed">Feed</Tabs.Trigger>
                <Tabs.Trigger value="FriendList">Friend list</Tabs.Trigger>
            {/if}
            {#each content as tab}
                <Tabs.Trigger value={tab.tab_value}>{tab.tab_name}</Tabs.Trigger
                >
            {/each}
        </Tabs.List>
        <Tabs.Content value="account">
            <Card.Root>
                <Card.Header>
                    <Card.Title>Account</Card.Title>
                    {#if isFriend === friendStatus.ME}
                        <Card.Description>
                            Check your account information here
                        </Card.Description>
                    {/if}
                </Card.Header>
                <Card.Content class="space-y-2">
                    {#if isFriend === friendStatus.ME}
                        <div class="space-y-1">
                            <Label>Email</Label>
                            <p>{user.email}</p>
                        </div>
                        <div class="space-y-1">
                            <Label>Username</Label>
                            <p>{user.username}</p>
                        </div>
                    {:else if isFriend === friendStatus.FRIEND}
                        <Button
                            class="bg-rich_black/75 text-white hover:bg-rich_black "
                            on:click={async () => {
                                let response = await fetch(
                                    `${apiKey}/friends/remove`,
                                    {
                                        method: "POST",
                                        headers: {
                                            "Content-Type": "application/json",
                                            Authorization: `Bearer ${token}`,
                                        },
                                        body: JSON.stringify({
                                            email: user.email,
                                        }),
                                    },
                                );
                                if (!response.ok) {
                                    console.error("Could not remove friend");
                                }
                                isFriend = friendStatus.STRANGER;
                            }}>Remove this friend</Button
                        >
                    {:else}
                        <Button
                            class="bg-white text-rich_black hover:text-white"
                            on:click={async () => {
                                let response = await fetch(
                                    `${apiKey}/friends/request`,
                                    {
                                        method: "POST",
                                        headers: {
                                            "Content-Type": "application/json",
                                            Authorization: `Bearer ${token}`,
                                        },
                                        body: JSON.stringify({
                                            email: user.email,
                                        }),
                                    },
                                );
                                if (!response.ok) {
                                    console.error(
                                        "Could not send friend request",
                                    );
                                }
                                addFrientText = "Friend request sent!";
                            }}>{addFrientText}</Button
                        >
                    {/if}
                </Card.Content>
            </Card.Root>
        </Tabs.Content>
        {#if isFriend === friendStatus.ME}
            <Tabs.Content value="feed">
                <Card.Root>
                    <Card.Header>
                        <Card.Title>Feed</Card.Title>
                        <Card.Description>
                            Check out what your friends are doing!
                        </Card.Description>
                    </Card.Header>
                    <Card.Content class="space-y-2">
                        {#each user.feed as item}
                            <p>{item}</p>
                            <Separator />
                        {/each}
                    </Card.Content>
                </Card.Root>
            </Tabs.Content>
            <Tabs.Content value="FriendList">
                <Card.Root>
                    <Card.Header>
                        <Card.Title>Friend list</Card.Title>
                        <Card.Description>These are your pals</Card.Description>
                    </Card.Header>
                    <Card.Content class="space-y-2">
                        <div class="mb-8">
                            {#each reqs as req}
                                <Button
                                    class="bg-white text-rich_black hover:text-white"
                                    on:click={async () => {
                                        let response = await fetch(
                                            `${apiKey}/friends/respond`,
                                            {
                                                method: "POST",
                                                headers: {
                                                    "Content-Type":
                                                        "application/json",
                                                    Authorization: `Bearer ${token}`,
                                                },
                                                body: JSON.stringify({
                                                    email: req.sender,
                                                    response: "accept",
                                                }),
                                            },
                                        );
                                        if (!response.ok) {
                                            console.error(
                                                "Could not accept friend",
                                            );
                                        }
                                        reqs = reqs.filter(
                                            (r) => r.sender !== req.sender,
                                        );
                                    }}
                                >
                                    Accept friend request from {req.username}</Button
                                >
                                <Button
                                    class="bg-white text-rich_black hover:text-white"
                                    on:click={async () => {
                                        let response = await fetch(
                                            `${apiKey}/friends/respond`,
                                            {
                                                method: "POST",
                                                headers: {
                                                    "Content-Type":
                                                        "application/json",
                                                    Authorization: `Bearer ${token}`,
                                                },
                                                body: JSON.stringify({
                                                    email: req.sender,
                                                    response: "reject",
                                                }),
                                            },
                                        );
                                        if (!response.ok) {
                                            console.error(
                                                "Could not reject friend",
                                            );
                                        }
                                        reqs = reqs.filter(
                                            (r) => r.sender !== req.sender,
                                        );
                                    }}
                                >
                                    Reject friend request from {req.username}</Button
                                >
                            {/each}
                        </div>
                        {#each friends as friend}
                            <Separator />
                            <div
                                class="flex flex-row space-x-2 items-center text-end"
                            >
                                <a
                                    href="/profile/{friend.username}"
                                    rel="external"
                                    class="text-xl">{friend.username}</a
                                >
                                <p class="text-muted-foreground text-sm">
                                    friends since {friend.since}
                                </p>
                            </div>
                        {/each}
                    </Card.Content>
                </Card.Root>
            </Tabs.Content>
        {/if}
        {#each content as tab}
            <Tabs.Content value={tab.tab_value}>
                <Card.Root>
                    <Card.Header>
                        <Card.Title>{tab.tab_name}</Card.Title>
                        <Card.Description>
                            {tab.description}
                        </Card.Description>
                    </Card.Header>
                    <Card.Content class="space-y-2">
                        {#if tab.data.length === 0}
                            <p>There is no content in this section :(</p>
                        {:else}
                            {#each tab.data as media}
                                <Separator class="my-2" />
                                <div class="flex flex-row space-x-4">
                                    <img
                                        src={media.poster}
                                        alt={media.data.title ||
                                            media.data.name}
                                        class="h-48 w-fit"
                                    />

                                    <div class="flex flex-col">
                                        <a
                                            href="/{tab.media_type}/{media.data
                                                .id}"
                                            class="text-4xl"
                                            >{media.data.title ||
                                                media.data.name}</a
                                        >
                                        {#if media.rating}
                                            <p>Your rating: {media.rating}</p>
                                        {/if}
                                    </div>
                                </div>
                            {/each}
                        {/if}
                    </Card.Content>
                </Card.Root>
            </Tabs.Content>
        {/each}
    </Tabs.Root>
{/if}
