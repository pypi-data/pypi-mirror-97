ptee
=============================================

something like `tee` but support rotate logs




Usage
-------------------------------------------------

watch dir
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

.. code-block::

    cqh_tail --pattern=~/**/*.log

watch dir and filter
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

.. code-block::

    cqh_tail --pattern=~/**/*.log --line-filter="\.general/"
