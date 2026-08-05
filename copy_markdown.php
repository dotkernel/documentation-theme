<?php
/**
 * Copies the source Markdown files into the generated site, so every page is
 * also available in its original Markdown form.
 *
 * `docs/book/v7/introduction/introduction.md` is copied to
 * `docs/html/v7/introduction/introduction.md`, making it available as
 * `<site_url>/v7/introduction/introduction.md`, next to the generated
 * `<site_url>/v7/introduction/introduction/` page.
 *
 * This must run after `mkdocs build --clean`, as that empties the output
 * directory.
 */

$docPath = $argv[1] ?? 'docs';
$docPath = sprintf('%s/%s', getcwd(), $docPath);
$docPath = realpath($docPath);

$sourcePath = $docPath . '/book';
$targetPath = $docPath . '/html';

if (! is_dir($sourcePath)) {
    printf("[FAILED] Documentation directory '%s' does not exist\n", $sourcePath);
    exit(1);
}

if (! is_dir($targetPath)) {
    printf("[FAILED] Output directory '%s' does not exist; run this after mkdocs build\n", $targetPath);
    exit(1);
}

$rdi = new RecursiveDirectoryIterator($sourcePath, FilesystemIterator::SKIP_DOTS);
$rii = new RecursiveIteratorIterator($rdi, RecursiveIteratorIterator::SELF_FIRST);
$files = new RegexIterator($rii, '/\.md$/', RecursiveRegexIterator::GET_MATCH);

$copied = 0;

$process = function () use ($files, $sourcePath, $targetPath, &$copied) {
    $fileInfo = $files->getInnerIterator()->current();
    if (! $fileInfo->isFile()) {
        return true;
    }

    $source = $fileInfo->getPathname();
    $target = $targetPath . substr($source, strlen($sourcePath));

    $targetDir = dirname($target);
    if (! is_dir($targetDir) && ! mkdir($targetDir, 0755, true)) {
        printf("[FAILED] Could not create directory '%s'\n", $targetDir);
        exit(1);
    }

    if (! copy($source, $target)) {
        printf("[FAILED] Could not copy '%s' to '%s'\n", $source, $target);
        exit(1);
    }

    $copied++;

    return true;
};

iterator_apply($files, $process);

printf("Copied %d Markdown file(s) into %s\n", $copied, $targetPath);
