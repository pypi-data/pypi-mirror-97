Model
=====

.. currentmodule:: pykeen.models

.. autoclass:: Model
   :show-inheritance:

   .. rubric:: Attributes Summary

   .. autosummary::

      ~Model.can_slice_h
      ~Model.can_slice_r
      ~Model.can_slice_t
      ~Model.loss_default_kwargs
      ~Model.num_entities
      ~Model.num_parameter_bytes
      ~Model.num_relations

   .. rubric:: Methods Summary

   .. autosummary::

      ~Model.compute_loss
      ~Model.get_all_prediction_df
      ~Model.get_grad_params
      ~Model.get_head_prediction_df
      ~Model.get_relation_prediction_df
      ~Model.get_tail_prediction_df
      ~Model.load_state
      ~Model.post_forward_pass
      ~Model.post_parameter_update
      ~Model.predict_h
      ~Model.predict_hrt
      ~Model.predict_r
      ~Model.predict_t
      ~Model.reset_parameters_
      ~Model.save_state
      ~Model.score_h
      ~Model.score_h_inverse
      ~Model.score_hrt
      ~Model.score_hrt_inverse
      ~Model.score_r
      ~Model.score_t
      ~Model.score_t_inverse
      ~Model.to_device_

   .. rubric:: Attributes Documentation

   .. autoattribute:: can_slice_h
   .. autoattribute:: can_slice_r
   .. autoattribute:: can_slice_t
   .. autoattribute:: loss_default_kwargs
   .. autoattribute:: num_entities
   .. autoattribute:: num_parameter_bytes
   .. autoattribute:: num_relations

   .. rubric:: Methods Documentation

   .. automethod:: compute_loss
   .. automethod:: get_all_prediction_df
   .. automethod:: get_grad_params
   .. automethod:: get_head_prediction_df
   .. automethod:: get_relation_prediction_df
   .. automethod:: get_tail_prediction_df
   .. automethod:: load_state
   .. automethod:: post_forward_pass
   .. automethod:: post_parameter_update
   .. automethod:: predict_h
   .. automethod:: predict_hrt
   .. automethod:: predict_r
   .. automethod:: predict_t
   .. automethod:: reset_parameters_
   .. automethod:: save_state
   .. automethod:: score_h
   .. automethod:: score_h_inverse
   .. automethod:: score_hrt
   .. automethod:: score_hrt_inverse
   .. automethod:: score_r
   .. automethod:: score_t
   .. automethod:: score_t_inverse
   .. automethod:: to_device_
