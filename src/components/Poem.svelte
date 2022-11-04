<script>
    import poems from "src/poems";

    let show_full_poem = false;
    let selected_poem = poems[Math.floor(Math.random() * poems.length)];

    // preview
    let safe_content = selected_poem.content.filter((content) => content.length > 0);
    let preview = safe_content[Math.floor(Math.random() * safe_content.length)].replace("&nbsp", "");

    let show_poem_list = false;

    /** @type {HTMLElement} */
    let poem_content = undefined;
</script>

<div class="poem">
    {#if show_full_poem == false}
        <a
            href="/show-full"
            on:click="{(event) => {
                event.preventDefault();
                show_full_poem = true;
                setTimeout(() => {
                    poem_content.scrollIntoView({
                        behavior: 'smooth',
                    });
                }, 100);
            }}">
            {preview}<br />
            <sub>{selected_poem.author} - {selected_poem.title}</sub>
        </a>
    {:else if show_poem_list == true}
        <div class="lf">
            <ol class="list">
                {#each poems as poem}
                    <li>
                        <a
                            href="/select"
                            on:click="{(event) => {
                                event.preventDefault();

                                show_poem_list = false;
                                selected_poem = poem;

                                setTimeout(() => {
                                    poem_content.scrollIntoView({
                                        behavior: 'smooth',
                                    });
                                }, 100);
                            }}">{poem.author} - {poem.title}</a>
                    </li>
                {/each}
            </ol>
        </div>
    {:else}
        <div class="lf poem-content" bind:this="{poem_content}">
            <h2>{selected_poem.title}</h2>
            <h3>
                <a
                    href="/author"
                    on:click="{(event) => {
                        event.preventDefault();
                        show_poem_list = true;
                    }}">{selected_poem.author}</a>
            </h3>
            {#each selected_poem.content as content}
                <span>{@html content}</span><br />
            {/each}
        </div>
    {/if}
</div>

<style>
    .poem {
        text-align: center;
        margin-top: 60px;
    }

    .poem-content > h2 {
        margin: 0;
    }

    .poem-content > h3 {
        margin-top: 0;
    }
</style>
