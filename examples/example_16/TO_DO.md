## List of task to be done:

( **boldface** - do this before sending e-mail around)

- **coordinates - to allow parallax fits**
- MulensData - just provide *str*
- remove _update_best_model() and extract it from fitting results
- binary source and number of fluxes returned - see _return_ln_prob()
- all_parameters in _get_parameters_ordered() and _check_fixed_parameters() - combine in a single one
- note that parameters are re-ordered (maybe in future add option for specifying order)
- datasets - guessing 245/246
- **data here for tests, so that PATH doesnt change**
- no_negative_blending_flux - only first dataset, or all datasets? Maybe add one more option
- **limit epochs in "best model" plot**
- **limit Y axis in "best model" plot**
- trace plot
- **methods for Model**
- self._plots - check what is there
- Fitting method to be added: scipy.optimize, pymultinest, ???
- for plots: t_0, \Delta t_0, or t_0 - 2456780 ???
- should version be printed on output?
- allow plotting many models from posterior
- MulensData() - use try/except with meaningful error message
- Add ln_prior values to blob? At some point we will want to save that information in output files
- settings['input_file_root'] = input_file_root - in final function and use it for default output files names
- check if output files (including plots) exists at the begin
- add check if 't_0' is covered by data and give warning if not
