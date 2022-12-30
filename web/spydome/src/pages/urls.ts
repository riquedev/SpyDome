import type {Router} from "next/router";
import type {PrefetchOptions} from "next/dist/shared/lib/router/router";
import type {UrlObject} from "url";

const pageLocations = {
    index: '/',
    dome: {
        index: '/'
    }
}

declare type Url = UrlObject | string;

interface TransitionOptions {
    shallow?: boolean;
    locale?: string | false;
    scroll?: boolean;
    unstable_skipClientCache?: boolean;
}

interface prefetchParams {
    url: string,
    asPath?: string,
    options?: PrefetchOptions
}

interface pushParams {
    url: Url,
    as?: Url,
    options?: TransitionOptions
}

export function prefetch(router: Router, {url, asPath, options}: prefetchParams): Promise<void> {
    /**
     * Prefetch pages for faster client-side transitions.
     * This method is only useful for navigations without next/link,
     * as next/link takes care of prefetching pages automatically.
     */
    return router.prefetch(url, asPath, options);
}

export function back(router: Router): void {
    /**
     * Navigate back in history. Equivalent to clicking
     * the browser’s back button. It executes window.history.back().
     */
    return router.back()
}

export function reload(router: Router): void {
    /**
     * Reload the current URL. Equivalent to clicking
     * the browser’s refresh button. It executes window.location.reload().
     */
    return router.reload()
}

export function push(router: Router, {url, options, as}: pushParams): Promise<boolean> {
    /**
     * Handles client-side transitions, this method is
     * useful for cases where next/link is not enough.
     */
    return router.push(url, as, options);
}

export function getUrl(path: string): string {
    return Object(pageLocations).get(path)
}

/**
 * Go to methods
 */

export async function goToIndex(router: Router, usePrefetch: boolean = true) {
    const url = getUrl("index");
    if (usePrefetch) {
        await prefetch(router, {url});
    }
    return await push(router, {url})
}

export async function gotoDomeIndex(router: Router, usePrefetch: boolean = true){
    const url = getUrl("dome.index");
    if (usePrefetch) {
        await prefetch(router, {url});
    }
    return await push(router, {url})
}
