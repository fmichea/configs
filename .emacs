;; Main emacs configuration of Franck "kushou" Michea

;; Load Paths
(setq load-path (cons "~/.emacs.d" load-path))
(setq load-path (cons "~/.emacs.d/tuareg-mode" load-path))

;; Own Modes Requires
;(require 'haskell-mode)
(require 'lua-mode)
(require 'php-mode)
(require 'python-mode)
(require 'scss-mode)
(require 'tuareg)

;; Main configuration
(column-number-mode t)

(setq-default show-trailing-whitespace t)
(add-hook 'before-save-hook 'delete-trailing-whitespace)

(setq c-default-style "bsd")
(setq c-basic-offset 2)

(show-paren-mode t)

;; Keyboard bindings

(global-set-key [M-left] 'windmove-left)
(global-set-key [M-right] 'windmove-right)
(global-set-key [M-up] 'windmove-up)
(global-set-key [M-down] 'windmove-down)

;; File extension -> mode
(add-to-list 'auto-mode-alist '("\\.lua$" . lua-mode))
(add-to-list 'auto-mode-alist '("\\.php[345]?$" . php-mode))
(add-to-list 'auto-mode-alist '("\\.py$" . python-mode))
(add-to-list 'auto-mode-alist '("\\.scss$" . scss-mode))
(add-to-list 'auto-mode-alist '("\\.ml\\w?$" . tuareg-mode))

;; Insert header guard in C/C++ header file
;; the recognized extensions are .h, .hh or .hxx

(defun insert-header-guard ()
  (interactive)
  (if (string-match "\\.h\\(h\\|xx\\)?$" (buffer-name))
      (let ((header-guard
             (upcase (replace-regexp-in-string "[-.]" "_" (buffer-name)))))
        (save-excursion
          (goto-char (point-min))
          (insert "#ifndef " header-guard "\n")
          (insert "# define " header-guard "\n\n")
          (goto-char (point-max))
          (insert "\n#endif /* !" header-guard " */")))
    (message "Invalid C/C++ header file.")))

(if (file-exists-p "~/.emacs_opt")
    (load-file "~/.emacs_opt"))

;; EOF