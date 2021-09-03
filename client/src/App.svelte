<script>
  import { onMount } from "svelte";
  import SvelteList from "./components/list.svelte";
  import { Button } from "sveltestrap";

  let config = null;

  $: invalidPrefix = config && config.command_prefix == "";

  let prefixChanged = false;
  let commandsChanged = false;
  let triggersChanged = false;

  async function setup() {
    config = await fetch("/api/config").then((d) => d.json());
  }

  async function update() {
    await fetch("/api/update", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(config),
    });

    commandsChanged = triggersChanged = prefixChanged = false;
  }

  onMount(async () => {
    setup();
  });
</script>

{#if config}
  <div class="container">
    <span>Command Prefix: </span>
    <input
      type="text"
      bind:value={config.command_prefix}
      on:input={() => (prefixChanged = true)}
      class:invalid={invalidPrefix}
    />
    <br />
    <div class="float-start">
      <SvelteList
        items={config.commands}
        title="Commands:"
        bind:changed={commandsChanged}
      />
      <br />
      <SvelteList
        items={config.triggers}
        title="Triggers:"
        bind:changed={triggersChanged}
      />
      {#if (commandsChanged || triggersChanged || prefixChanged) && !invalidPrefix}
        <div class="float-end">
          <Button on:click={update} color="primary">Update</Button>
        </div>
      {/if}
    </div>
  </div>
{:else}
  <span>There is no config!!!!!!</span>
{/if}

<style>
  .invalid {
    border-color: red;
  }
</style>
