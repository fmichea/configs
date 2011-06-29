;; Main emacs configuration of Franck "kushou" Michea

;; Load Paths
(setq load-path (cons "~/.emacs.d" load-path))
(setq load-path (cons "~/.emacs.d/haskell-mode" load-path))
(setq load-path (cons "~/.emacs.d/tuareg-mode" load-path))

;; Default Requires
(require 'ido)

;; Own Modes Requires
(require 'haskell-mode)
(require 'lua-mode)
(require 'php-mode)
(require 'python-mode)
(require 'scss-mode)
(require 'tuareg)

;; Main configuration
(column-number-mode t)
(ido-mode t)

;; C configuration
(setq c-default-style "bsd")
(setq c-basic-offset 2)

;; File extension -> mode
(add-to-list 'auto-mode-alist '("\\.hs$" . haskell-mode))
(add-to-list 'auto-mode-alist '("\\.lua$" . lua-mode))
(add-to-list 'auto-mode-alist '("\\.php[345]?$" . php-mode))
(add-to-list 'auto-mode-alist '("\\.py$" . python-mode))
(add-to-list 'auto-mode-alist '("\\.scss$" . scss-mode))
(add-to-list 'auto-mode-alist '("\\.ml\\w?$" . tuareg-mode))
