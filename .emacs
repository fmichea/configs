;; Global Configuration

;;(column-number-mode t)

;; PHP Configuration
;;(add-to-list 'load-path "~/.emacs.d/php-mode")
;;(autoload 'php-mode "php-mode.el" "Php mode." t)
;;

;; OCaml Configuration
;;(add-to-list 'load-path "~/.emacs.d/tuareg-mode")
;;(setq auto-mode-alist (cons '("\\.ml\\w?" . tuareg-mode) auto-mode-alist))
;;(autoload 'tuareg-mode "tuareg" "Major mode for editing Caml code" t)
;;(autoload 'camldebug "camldebug" "Run the Caml debugger" t)

;; Haskell Configuration (FIXME)
;; Error: File mode specification error: (void-function haskell-mode)

;;(add-to-list 'load-path "~/.emacs.d/haskell-mode")
;;(setq auto-mode-alist (cons '("\\.hs$" . haskell-mode) auto-mode-alist))

;; LUA Configuration

;;(add-to-list 'load-path "~/.emacs.d/lua-mode")
;;(setq auto-mode-alist (cons '("\.lua$" . lua-mode) auto-mode-alist))
;;(autoload 'lua-mode "lua-mode" "Lua editing mode." t)

;; C Configuration

;;(setq c-default-style "bsd")
;;(setq c-basic-offset 2)

;; Python Configuration
;;(add-to-list 'load-path "~/.emacs.d/python-mode")
;;(autoload 'python-mode "python-mode" "Python Mode." t)
;;(add-to-list 'auto-mode-alist '("\\.py\\'" . python-mode))
;;(add-to-list 'interpreter-mode-alist '("python" . python-mode))

;; highlight trailing whitespace
;;(setq-default show-trailing-whitespace t)
;;(add-hook 'before-save-hook 'delete-trailing-whitespace)

;; SCSS Hilighting
;;(add-to-list 'load-path "~/.emacs.d/scss-mode.el")

;; highlight long lines
;;(setq whitespace-style '(lines))
;;(setq whitespace-line-column 79)
;;(global-whitespace-mode 1)
;; Doxymacs
;;(add-to-list 'load-path "~/.emacs.d/doxymacs")
;;(require 'doxymacs)


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
