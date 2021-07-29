;;; (load (compile-file "bt1.lisp"))

;;; First try at a peak chaser. The goal isn't just to peak chase, but
;;; to compare peak-chasing models for their human-in-the-loop
;;; efficiency.

;;; The peak being "chased" tends toward the center, but occassionally
;;; walks away for a while before settling into a new center. We use
;;; -1...+1 as the possible range. If it hits the end limits, the
;;; thing simply terminates (or resets).

(defparameter *hits* 0)
(defparameter *misses* 0)

(defparameter *max-cycles* 10000)
(defparameter *stream-shift-time-slice* 100)
(defparameter *stream-p-shift* 0.05)
(defparameter *stream-shift-amount* 0.01)
(defparameter *beam-shift-amount* (* 0.05 *stream-shift-amount*))
(defparameter *stream-shift-low-rand-int* (truncate (* *stream-shift-time-slice* *stream-p-shift*)))
(defparameter *beam-pos* 0.0)

(defparameter *operator-response-delay* 0) ;; cycles

(defun run-stream (&key (show? nil) (tracking-strategy :directed-shift))
  (setf *hits* 0 *misses* 0)
  (loop with stream-pos = 0.0
	with beam-pos = 0.0
	with allow-response-cycle = 99999999999
	as cycle from 1 by 1
	until (or (= cycle *max-cycles*) (>= (abs stream-pos) 1.0)) ;; Stop if it goes outside the wall
	do (if (< (random *stream-shift-time-slice*) *stream-shift-low-rand-int*)
	       (setf stream-pos (trunc2 (+ stream-pos (* *stream-shift-amount* (if (zerop (random 2)) +1 -1))))
		     allow-response-cycle (+ cycle *operator-response-delay*)))
	(showpos stream-pos beam-pos show?)
	(if (>= cycle allow-response-cycle)
	    (setf beam-pos (trunc2 (track stream-pos beam-pos tracking-strategy))))
	(when (= beam-pos stream-pos (setf allow-response-cycle 99999999999)))
	)
  (format t "============================================~%Hits=~a, Misses=~a, Win fraction=~a~%"
	  *hits* *misses* (float (/ *hits* (+ *hits* *misses*)))))

(defun trunc2 (n)
  (/ (truncate (* n 100)) 100))

(defun track (stream-pos beam-pos tracking-strategy)
  (case tracking-strategy
	(:static beam-pos)
	(:random-shift (if (zerop (random 2)) (+ beam-pos (* *stream-shift-amount* (if (zerop (random 2)) +1 -1))) beam-pos))
	(:directed-shift (if (= beam-pos stream-pos) beam-pos (+ beam-pos (* *beam-shift-amount* (if (> stream-pos beam-pos) +1 -1)))))
	(t (error "In TRACK: Invalid tracking strategy: ~a" tracking-strategy))))

(defparameter *show-width* 40)
(defparameter *show-incr* (/ 2.0 *show-width*))

(defun showpos (stream-pos beam-pos show?)
  (when show? (format t "["))
  (loop for i below *show-width*
	with beam-shown? = nil
	with stream-shown? = nil
	as miss = nil
	as sp from -1.0 by *show-incr*
	do
	;; We have to go through the motions here in order to update the stats!
	(let ((char 
	       (cond ((and stream-shown? beam-shown?) " ")
		     ((and (not stream-shown?) (not beam-shown?) (>= sp stream-pos) (>= sp beam-pos)) (setf stream-shown? t) (setf beam-shown? t)
		      (incf *hits*) (setf hit t) "*")
		     ((and (not stream-shown?) (>= sp stream-pos)) (setf stream-shown? t) (incf *misses*) "|")
		     ((and (not beam-shown?) (>= sp beam-pos)) (setf beam-shown? t) (incf *misses*) "x")
		     (t " "))))
	  (when show? (format t "~a " char)))
	finally (when show? (format t "] s:~,2f, b:~,2f~%" stream-pos beam-pos))))

(defun run (&key (show? nil))
  (loop for *operator-response-delay* from 0 to 10 by 1
	do (format t "~% *operator-response-delay* = ~a~%" *operator-response-delay*)
	(run-stream :show? show?)))

(run :show? t)
