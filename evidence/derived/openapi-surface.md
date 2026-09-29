# Public OpenAPI specifications

Captured unauthenticated by the probe script. Path counts and parameter diffs are computed
mechanically from each specification; descriptions are quoted from the spec.

## Baseten management API

Title: Baseten management API; version: 1.0.0; OpenAPI 3.1.0; servers: https://api.baseten.co.

Paths: 160; operations: 211; security schemes: BearerAuth.

<details><summary>Path list</summary>

| Methods | Path |
| --- | --- |
| GET | `/v1/volumes` |
| POST | `/v1/volumes/token` |
| GET | `/v1/volumes/namespaces` |
| GET,POST | `/v1/volumes/syncs` |
| GET | `/v1/volumes/syncs/{volume_sync_id}` |
| POST | `/v1/volumes/syncs/{volume_sync_id}/cancel` |
| DELETE,GET | `/v1/volumes/{volume_namespace}/{volume_name}` |
| GET | `/v1/volumes/{volume_namespace}/{volume_name}/versions` |
| DELETE,GET | `/v1/volumes/{volume_namespace}/{volume_name}/versions/{volume_version}` |
| POST | `/v1/volumes/{volume_namespace}/{volume_name}/versions/{volume_version}/restore` |
| POST | `/v1/token` |
| GET,POST | `/v1/secrets` |
| DELETE | `/v1/secrets/{secret_name}` |
| GET,POST | `/v1/teams/{team_id}/secrets` |
| DELETE | `/v1/teams/{team_id}/secrets/{secret_name}` |
| GET | `/v1/environment_groups` |
| GET,PATCH | `/v1/environment_groups/{env_name}` |
| GET | `/v1/teams/{team_id}/environment_groups` |
| GET,PATCH | `/v1/teams/{team_id}/environment_groups/{env_name}` |
| GET | `/v1/teams` |
| GET | `/v1/teams/{team_id}` |
| GET | `/v1/regions` |
| GET | `/v1/teams/{team_id}/regions` |
| GET | `/v1/instance_types` |
| GET,PATCH | `/v1/loops/user_config` |
| GET | `/v1/instance_type_prices` |
| POST | `/v1/prepare_model_upload` |
| GET | `/v1/audit_logs` |
| GET,POST | `/v1/models` |
| GET,POST | `/v1/teams/{team_id}/models` |
| DELETE,GET,PATCH | `/v1/models/{model_id}` |
| GET | `/v1/models/{model_id}/audit_logs` |
| GET,POST | `/v1/models/{model_id}/deployments` |
| GET | `/v1/models/{model_id}/deployments/development` |
| GET | `/v1/models/{model_id}/deployments/production` |
| DELETE,GET,PATCH | `/v1/models/{model_id}/deployments/{deployment_id}` |
| PATCH | `/v1/models/{model_id}/deployments/development/autoscaling_settings` |
| PATCH | `/v1/models/{model_id}/deployments/production/autoscaling_settings` |
| PATCH | `/v1/models/{model_id}/deployments/{deployment_id}/autoscaling_settings` |
| PATCH | `/v1/models/{model_id}/deployments/{deployment_id}/request_backpressure_settings` |
| POST | `/v1/models/{model_id}/deployments/development/promote` |
| POST | `/v1/models/{model_id}/deployments/{deployment_id}/promote` |
| POST | `/v1/models/{model_id}/deployments/development/activate` |
| POST | `/v1/models/{model_id}/deployments/production/activate` |
| POST | `/v1/models/{model_id}/deployments/{deployment_id}/activate` |
| POST | `/v1/models/{model_id}/deployments/development/deactivate` |
| POST | `/v1/models/{model_id}/deployments/production/deactivate` |
| POST | `/v1/models/{model_id}/deployments/{deployment_id}/deactivate` |
| POST | `/v1/models/{model_id}/deployments/development/retry` |
| POST | `/v1/models/{model_id}/deployments/production/retry` |
| POST | `/v1/models/{model_id}/deployments/{deployment_id}/retry` |
| GET | `/v1/models/{model_id}/deployments/{deployment_id}/download` |
| GET | `/v1/models/{model_id}/deployments/{deployment_id}/config` |
| GET,POST | `/v1/models/{model_id}/deployments/{deployment_id}/logs` |
| POST | `/v1/models/{model_id}/deployments/{deployment_id}/patches` |
| GET | `/v1/models/{model_id}/deployments/{deployment_id}/patches/state` |
| POST | `/v1/models/{model_id}/deployments/{deployment_id}/patches/sync` |
| GET | `/v1/models/{model_id}/deployments/{deployment_id}/metrics` |
| DELETE | `/v1/models/{model_id}/deployments/{deployment_id}/replicas/{replica_id}` |
| POST | `/v1/models/{model_id}/deployments/{deployment_id}/ssh/sign` |
| GET,POST | `/v1/models/{model_id}/environments` |
| DELETE,GET,PATCH | `/v1/models/{model_id}/environments/{env_name}` |
| GET | `/v1/models/{model_id}/environments/{env_name}/logs` |
| GET | `/v1/models/{model_id}/environments/{env_name}/metrics` |
| POST | `/v1/models/{model_id}/environments/{env_name}/activate` |
| POST | `/v1/models/{model_id}/environments/{env_name}/deactivate` |
| POST | `/v1/models/{model_id}/environments/{env_name}/promote` |
| POST | `/v1/models/{model_id}/environments/{env_name}/cancel_promotion` |
| POST | `/v1/models/{model_id}/environments/{env_name}/pause_promotion` |
| POST | `/v1/models/{model_id}/environments/{env_name}/resume_promotion` |
| POST | `/v1/models/{model_id}/environments/{env_name}/force_cancel_promotion` |
| POST | `/v1/models/{model_id}/environments/{env_name}/force_roll_forward_promotion` |
| GET | `/v1/chains` |
| DELETE,GET | `/v1/chains/{chain_id}` |
| GET | `/v1/chains/{chain_id}/audit_logs` |
| GET | `/v1/chains/{chain_id}/deployments` |
| DELETE,GET | `/v1/chains/{chain_id}/deployments/{chain_deployment_id}` |
| POST | `/v1/chains/{chain_id}/deployments/{chain_deployment_id}/deactivate` |
| GET | `/v1/chains/{chain_id}/deployments/{chain_deployment_id}/chainlets/{chainlet_id}/logs` |
| GET,POST | `/v1/chains/{chain_id}/environments` |
| GET,PATCH | `/v1/chains/{chain_id}/environments/{env_name}` |
| POST | `/v1/chains/{chain_id}/environments/{env_name}/promote` |
| PATCH | `/v1/chains/{chain_id}/environments/{env_name}/chainlet_settings/autoscaling_settings` |
| POST | `/v1/chains/{chain_id}/environments/{env_name}/chainlet_settings/instance_types/update` |
| POST | `/v1/teams/{team_id}/training_projects` |
| GET,POST | `/v1/training_projects` |
| GET,POST | `/v1/training_projects/{training_project_id}/jobs` |
| DELETE,GET,PATCH | `/v1/training_projects/{training_project_id}/jobs/{training_job_id}` |
| GET | `/v1/training_projects/{training_project_id}/jobs/{training_job_id}/download` |
| POST | `/v1/training_projects/{training_project_id}/jobs/{training_job_id}/recreate` |
| GET,POST | `/v1/training_projects/{training_project_id}/jobs/{training_job_id}/logs` |
| GET,POST | `/v1/training_projects/{training_project_id}/jobs/{training_job_id}/metrics` |
| POST | `/v1/training_projects/{training_project_id}/jobs/{training_job_id}/stop` |
| GET | `/v1/training_projects/{training_project_id}/jobs/{training_job_id}/checkpoints` |
| GET | `/v1/training_projects/{training_project_id}/jobs/{training_job_id}/checkpoint_files` |
| GET | `/v1/training_projects/{training_project_id}/jobs/{training_job_id}/auth_codes` |
| PATCH | `/v1/training_projects/{training_project_id}/jobs/{training_job_id}/interactive_sessions/{session_id}` |
| POST | `/v1/training_projects/{training_project_id}/jobs/{training_job_id}/ssh/sign` |
| GET | `/v1/training_projects/{training_project_id}/cache/summary` |
| DELETE,GET | `/v1/training_projects/{training_project_id}` |
| POST | `/v1/training_jobs/search` |
| GET | `/v1/loops/capabilities` |
| POST | `/v1/loops/sessions` |
| GET | `/v1/loops/sessions/{session_id}` |
| GET,POST | `/v1/loops/runs` |
| POST | `/v1/loops/runs/{run_id}/deactivate` |
| GET | `/v1/loops/runs/{run_id}` |
| POST | `/v1/loops/trainers` |
| GET,POST | `/v1/loops/samplers` |
| GET | `/v1/loops/samplers/{sampler_id}` |
| GET | `/v1/loops/checkpoints` |
| POST | `/v1/loops/checkpoints/validate` |
| GET | `/v1/loops/checkpoints/{checkpoint_id}/files` |
| GET | `/v1/loops/checkpoints/{checkpoint_id}/source` |
| GET | `/v1/loops/deployments` |
| POST | `/v1/loops/deployments/{deployment_id}/deactivate` |
| GET | `/v1/loops/deployments/{deployment_id}` |
| GET | `/v1/loops/deployments/{deployment_id}/debug_archive/files` |
| POST | `/v1/loops/deployments/{deployment_id}/metrics` |
| GET | `/v1/loops/deployments/{deployment_id}/logs` |
| POST | `/v1/teams/{team_id}/loops/sessions` |
| GET,POST | `/v1/teams/{team_id}/loops/runs` |
| POST | `/v1/teams/{team_id}/loops/trainers` |
| GET,POST | `/v1/teams/{team_id}/loops/samplers` |
| GET,PATCH | `/v1/training/capacity` |
| GET | `/v1/training/jobs/{training_job_id}/queue_context` |
| GET | `/v1/blobs/credentials/model` |
| GET | `/v1/blobs/credentials/train` |
| POST | `/v1/teams/{team_id}/api_keys` |
| GET,POST | `/v1/api_keys` |
| DELETE | `/v1/api_keys/{api_key_prefix}` |
| GET | `/v1/model_apis` |
| GET | `/v1/model_apis/usage` |
| GET | `/v1/model_apis/{model_api_name}` |
| POST | `/v1/llm_models` |
| POST | `/v1/teams/{team_id}/llm_models` |
| POST | `/v1/llm_models/{model_id}/deployments` |
| GET,POST | `/v1/library_listings` |
| DELETE,GET,PATCH | `/v1/library_listings/{user_defined_listing_id}` |
| GET,POST | `/v1/library_listings/{user_defined_listing_id}/versions` |
| DELETE,GET,PATCH | `/v1/library_listings/{user_defined_listing_id}/versions/{version_tag}` |
| GET | `/v1/billing/model_apis` |
| GET | `/v1/billing/usage_summary` |
| GET | `/v1/billing/tool_call_usage` |
| GET | `/v1/users` |
| GET | `/v1/users/me` |
| GET | `/v1/users/{user_id}` |
| GET | `/v1/organizations/me` |
| GET | `/v1/gateway/events` |
| GET | `/v1/explore/metadata` |
| GET,POST | `/v1/routes` |
| GET | `/v1/routes/usage` |
| DELETE,GET,PATCH | `/v1/routes/{route_id}` |
| GET,POST | `/v1/gateway/endpoints` |
| DELETE,GET,PATCH | `/v1/gateway/endpoints/{endpoint_id}` |
| GET,POST | `/v1/gateway/groups` |
| GET,PATCH | `/v1/gateway/groups/{group_id}` |
| GET,POST | `/v1/gateway/groups/{group_id}/api_keys` |
| POST | `/v1/gateway/groups/{group_id}/api_keys/register` |
| GET | `/v1/gateway/groups/{group_id}/api_keys/{api_key_prefix}` |

</details>

## DeepInfra API

Title: DeepInfra API; version: 1.0.0; OpenAPI 3.1.0; servers: https://api.deepinfra.com.

Paths: 140; operations: 169; security schemes: HTTPBearer.

Tags by operation count: Dedicated Models (22), Authentication (17), Billing (16), Models (15), Agents (13), Account (11), Sandboxes (10), Files & Batches (9), LoRA Adapters (9), GPU Rentals (7), Text to Speech (7), Videos (6), Image Generation (4), Logs & Metrics (4), Audio (3), Chat Completions (3), Responses (3), Inference (2), System One (2), Tokenizer (2), Utilities (2), Embeddings (1), Text Completions (1)

<details><summary>Path list</summary>

| Methods | Path |
| --- | --- |
| GET | `/v1/metrics/live` |
| GET | `/cli/version` |
| GET,DELETE,PATCH | `/v1/me` |
| GET | `/v1/me/emails` |
| POST | `/v1/me/team_display_name` |
| GET | `/v1/me/rate_limit` |
| POST | `/v1/me/rate_limit/request` |
| POST | `/v1/deploy` |
| GET | `/v1/gpu_pool/gpu_types` |
| GET | `/v1/me/gpu_pool` |
| POST | `/v1/me/gpu_pool/request` |
| DELETE | `/v1/me/gpu_pool/request/{request_id}` |
| POST | `/deploy/hf/` |
| GET | `/deploy/llm/gpu_availability` |
| GET | `/deploy/llm/suggest_name` |
| GET | `/deploy/llm/standard_args` |
| GET | `/deploy/llm/presets` |
| POST | `/deploy/llm` |
| GET | `/deploy/list/` |
| GET | `/deploy/list` |
| GET | `/deploy/stats` |
| GET,PUT,DELETE | `/deploy/{deploy_id}` |
| GET | `/deploy/{deploy_id}/stats` |
| GET | `/deploy/{deploy_id}/stats2` |
| GET | `/deploy/{deploy_id}/config/history` |
| POST | `/deploy/{deploy_id}/config/history/{entry_id}/restore` |
| POST | `/deploy/{deploy_id}/stop` |
| POST | `/deploy/{deploy_id}/start` |
| GET | `/models/private/list` |
| POST | `/lora-model` |
| DELETE | `/lora-model/{lora_model_name}` |
| GET | `/model-families/names` |
| GET | `/model-families/{family_name}` |
| GET | `/models/list` |
| GET | `/models/deployment/list` |
| GET | `/models/lora/list` |
| GET | `/openrouter/models` |
| POST | `/models/{model_name}/publicity` |
| POST | `/models/{model_name}/meta` |
| DELETE,GET | `/models/{model_name}` |
| GET | `/models/featured` |
| GET | `/models/{model_name}/schema/{variantKey}` |
| POST | `/v1/inference/deploy/{deploy_id}` |
| POST | `/v1/inference/{model_name}` |
| POST | `/v1/tokenize` |
| POST | `/v1/detokenize` |
| GET | `/v1/models` |
| POST | `/v1/images/generations` |
| POST | `/v1/images/variations` |
| POST | `/v1/images/edits` |
| POST | `/v1/feedback` |
| POST | `/v1/audio/speech` |
| POST | `/v1/audio/transcriptions` |
| POST | `/v1/audio/translations` |
| POST | `/v1/videos` |
| POST | `/v1/openai/videos` |
| GET | `/v1/videos/{video_id}` |
| GET | `/v1/openai/videos/{video_id}` |
| GET | `/v1/videos/{video_id}/content` |
| GET | `/v1/openai/videos/{video_id}/content` |
| GET | `/v1/logs/query` |
| GET | `/v1/deployment_logs/query` |
| GET | `/v1/voices` |
| POST | `/v1/text-to-speech/{voice_id}/stream` |
| POST | `/v1/text-to-speech/{voice_id}` |
| GET,DELETE | `/v1/voices/{voice_id}` |
| POST | `/v1/voices/add` |
| POST | `/v1/voices/{voice_id}/edit` |
| POST | `/v1/lora/create` |
| GET | `/v1/lora/{lora_name}/status` |
| GET,PATCH,DELETE | `/v1/lora/{lora_name}` |
| GET | `/v1/model/{model_name}/loras` |
| GET | `/v1/user/loras` |
| GET | `/v1/containers/params` |
| GET | `/v1/containers/gpu_availability` |
| POST,GET | `/v1/containers` |
| GET,PATCH,DELETE | `/v1/containers/{container_id}` |
| POST | `/v1/request-costs` |
| GET | `/v2/hardware` |
| POST | `/v1/completions` |
| POST | `/v1/chat/completions` |
| POST | `/v1/responses` |
| DELETE,GET | `/v1/responses/{response_id}` |
| POST | `/v1/embeddings` |
| POST | `/anthropic/v1/messages` |
| POST | `/anthropic/v1/messages/count_tokens` |
| POST | `/typesafe/v1/systemone` |
| GET | `/typesafe/v1/models` |
| GET | `/github/login` |
| GET | `/okta/login` |
| GET | `/github/cli/login` |
| GET | `/google/login` |
| GET,POST | `/v1/api-tokens` |
| GET,DELETE | `/v1/api-tokens/id/{token_id}` |
| GET,DELETE | `/v1/api-tokens/{api_token}` |
| POST | `/v1/api-tokens/vercel_export` |
| POST | `/v1/api-tokens/{api_token}/vercel_export` |
| POST,GET | `/v1/scoped-jwt` |
| GET,POST | `/v1/ssh_keys` |
| DELETE | `/v1/ssh_keys/{ssh_key_id}` |
| GET,POST | `/v1/files` |
| GET,DELETE | `/v1/files/{file_id}` |
| GET | `/v1/files/{file_id}/content` |
| GET | `/v1/images/{image_id}` |
| GET,POST | `/v1/batches` |
| GET | `/v1/batches/{batch_id}` |
| POST | `/v1/batches/{batch_id}/cancel` |
| POST,GET | `/deploy/{deploy_id}/rebalance` |
| POST | `/deploy/{deploy_id}/rebalance/cancel` |
| POST,GET | `/v1/agents` |
| GET | `/v1/agents/catalog` |
| GET,PATCH,DELETE | `/v1/agents/{instance_id}` |
| POST | `/v1/agents/{instance_id}/launch_token` |
| POST | `/v1/agents/{instance_id}/stop` |
| POST | `/v1/agents/{instance_id}/start` |
| POST | `/v1/agents/{instance_id}/update` |
| GET | `/v1/agents/{instance_id}/backups` |
| POST | `/v1/agents/{instance_id}/backup` |
| POST | `/v1/agents/{instance_id}/backups/{backup_id}/restore` |
| POST,GET | `/v1/sandboxes` |
| GET | `/v1/sandboxes/catalog` |
| GET,DELETE | `/v1/sandboxes/{sandbox_id}` |
| POST | `/v1/sandboxes/{sandbox_id}/stop` |
| POST | `/v1/sandboxes/{sandbox_id}/start` |
| POST | `/v1/sandboxes/{sandbox_id}/exec` |
| PUT,GET | `/v1/sandboxes/{sandbox_id}/fs/content` |
| GET | `/payment/checklist` |
| GET,POST | `/payment/config` |
| GET,POST | `/payment/key-limits` |
| GET | `/payment/billing-portal` |
| POST | `/payment/payment-methods/setup` |
| GET | `/payment/invoices` |
| GET | `/payment/usage` |
| GET | `/payment/usage/tokens` |
| GET | `/payment/usage/rent` |
| GET | `/payment/usage/id/{token_id}` |
| GET | `/payment/usage/{api_token}` |
| POST | `/payment/deepstart/application` |
| POST | `/payment/funds` |
| POST | `/payment/topup` |

</details>

### Chat completions request schema vs OpenAI (/v1/chat/completions)

Declared parameters: 31. Present OpenAI parameters: 20.

Parameters beyond the OpenAI schema:

| Parameter | Description (from spec) |
| --- | --- |
| `chat_template_kwargs` | Chat template kwargs. |
| `continue_final_message` | If set, the final assistant message is used as a prefix for the model to continue generating from, r |
| `fail_fast` | If true, the request is rejected immediately with HTTP 429 when the model has no spare capacity, ins |
| `ignore_eos` | Keep generating until max_tokens instead of stopping at the end-of-sequence token. Only honoured on  |
| `min_p` | Float that represents the minimum probability for a token to be considered, relative to the probabil |
| `models` | Ordered list of up to 4 fallback models. The request is attempted on each model in order: when a mod |
| `prompt_cache_options` | Prompt cache options for this request's prefix, e.g. {"ttl": "1h"}. |
| `reasoning` | Reasoning configuration. |
| `repetition_penalty` | Alternative penalty for repetition, but multiplicative instead of additive (> 1 penalize, < 1 encour |
| `stop_token_ids` | Up to 16 token IDs where the API will stop generating further tokens. Merged with the model's built- |
| `top_k` | Sample from the best k (number of) tokens. 0 means off |

OpenAI parameters absent from the schema: `audio`, `function_call`, `functions`, `logit_bias`, `max_completion_tokens`, `metadata`, `modalities`, `parallel_tool_calls`, `prediction`, `prompt_cache_retention`, `safety_identifier`, `store`, `top_logprobs`, `verbosity`, `web_search_options`

Documented response codes: 200 (Successful Response), 422 (Validation Error)

## Nebius Token Factory inference API

Title: Nebius OpenAI-compatible inference API; version: 20260928-144ca2fd4; OpenAPI 3.1.0; servers: https://api.tokenfactory.nebius.com.

Paths: 37; operations: 47; security schemes: HTTPBearer.

Tags by operation count: datasets (20), fine-tuning (9), files (6), inference (6), dedicated-endpoints (5), models (1)

<details><summary>Path list</summary>

| Methods | Path |
| --- | --- |
| POST | `/v1/completions` |
| POST | `/v1/chat/completions` |
| POST | `/v1/embeddings` |
| POST | `/v1/rerank` |
| POST | `/v1/responses` |
| GET | `/v1/models` |
| POST,GET | `/v1/files` |
| GET,DELETE | `/v1/files/{file_id}` |
| GET | `/v1/files/{file_id}/content` |
| GET | `/v1/files/{file_id}/link` |
| POST | `/v1/images/generations` |
| POST,GET | `/v1/fine_tuning/jobs` |
| GET | `/v1/fine_tuning/jobs/{job_id}` |
| POST | `/v1/fine_tuning/jobs/{job_id}/cancel` |
| GET | `/v1/fine_tuning/jobs/{job_id}/events` |
| GET | `/v1/fine_tuning/jobs/{job_id}/checkpoints` |
| GET | `/v1/fine_tuning/jobs/{job_id}/checkpoints/{checkpoint_id}` |
| GET | `/v1/fine_tuning/models/spec-draft` |
| GET | `/fine_tuning/models/spec-draft` |
| GET | `/v0/dedicated_endpoints/templates` |
| POST,GET | `/v0/dedicated_endpoints` |
| PATCH,DELETE | `/v0/dedicated_endpoints/{endpoint_id}` |
| POST,GET | `/v1/datasets` |
| GET,PATCH,DELETE | `/v1/datasets/{dataset_id}` |
| GET | `/v1/datasets/{dataset_id}/query_templates` |
| GET | `/v1/datasets/{dataset_id}/content` |
| GET | `/v1/datasets/{dataset_id}/export` |
| POST | `/v1/datasets/uploads` |
| POST,GET | `/v1/datasets/uploads/{upload_id}/parts` |
| POST | `/v1/datasets/uploads/{upload_id}/complete` |
| GET | `/v1/datasets/uploads/{upload_id}` |
| POST | `/v1/datasets/uploads/{upload_id}/cancel` |
| POST,GET | `/v1/operations` |
| GET | `/v1/operations/{operation_id}` |
| POST | `/v1/operations/{operation_id}/cancel` |
| GET | `/v1/operations/{operation_id}/results` |
| GET | `/v1/operations/{operation_id}/errors` |

</details>

### Chat completions request schema vs OpenAI (/v1/chat/completions)

Declared parameters: 23. Present OpenAI parameters: 22.

Parameters beyond the OpenAI schema:

| Parameter | Description (from spec) |
| --- | --- |
| `extra_body` | To provide extra parameters. |

OpenAI parameters absent from the schema: `audio`, `function_call`, `functions`, `metadata`, `modalities`, `parallel_tool_calls`, `prediction`, `prompt_cache_key`, `prompt_cache_retention`, `safety_identifier`, `seed`, `verbosity`, `web_search_options`

Documented response codes: 200 (OK), 400 (Bad request), 401 (Unauthorized), 402 (Payment required), 403 (Forbidden), 404 (Not found), 422 (Request validation failed), 429 (Rate limit exceeded), 500 (Internal server error), 503 (Inference service unavailable), 529 (Inference service overloaded)

## Akamai Cloud (Linode API v4)

Title: Akamai: Linode API; version: 4.215.0; OpenAPI 3.0.1; servers: https://api.linode.com.

Paths: 308; operations: 449; security schemes: oauth, personalAccessToken.

Tags by operation count: Image sharing (22), Databases (17), Linode instances (15), Firewalls (14), IP addresses (13), Buckets (12), Linode interfaces (10), Volumes (10), Clusters (9), Disks (8), Metrics (8), Nodes (8), Alerts (7), Domains (7), Images (7), Managed service monitors (7), Placement groups (7), Users (7), VPCs (7), Backups (6), Configuration profile interfaces (6), Configurations (6), Managed credentials (6), Node pools (6), NodeBalancers (6), OAuth clients (6), Object Storage (6), Payments (6), Access keys (5), Beta programs (5), Configuration profiles (5), Entity transfers (5), Longview clients (5), Managed contacts (5), Payment methods (5), Personal access tokens (5), Records (5), SSH keys (5), Service transfers (5), StackScripts (5), Statistics (5), VPC subnets (5), Credentials (4), Devices (4), IPv6 ranges (4), LKE versions (4), Logins (4), Regions (4), Support tickets (4), Tags (4), Account (3), Account settings (3), Child accounts (3), Control Plane ACL (3), Events (3), Invoices (3), Managed Linode settings (3), OAuth apps (3), Phone number (3), TLS/SSL certificates (3), Trusted devices (3), Two-factor authentication (3), Account agreements (2), Account availability (2), Advanced parameters (2), Engines (2), Firewall settings (2), IPv4 addresses (2), Kernels (2), Kubeconfigs (2), Linode types (2), Longview plans (2), Longview subscriptions (2), Managed issues (2), OAuth client (2), OAuth preferences (2), Profile (2), Replies (2), SSL certificates (2), Security questions (2), Templates (2), Types (2), VLANs (2), Account transfer (1), Attachments (1), Cluster dashboard (1), Domain zone file (1), Endpoints (1), Grants (1), IPv6 pools (1), LKE API endpoints (1), LKE service tokens (1), LKE types (1), Longview types (1), Maintenance policies (1), Maintenances (1), Managed SSH keys (1), Managed statistics (1), Network transfer prices (1), NodeBalancer types (1), Notifications (1), Promo credits (1), Volume types (1)

<details><summary>Path list</summary>

| Methods | Path |
| --- | --- |
| GET,PUT | `/{apiVersion}/account` |
| POST,GET | `/{apiVersion}/account/agreements` |
| GET | `/{apiVersion}/account/availability` |
| GET | `/{apiVersion}/account/availability/{regionId}` |
| POST,GET | `/{apiVersion}/account/betas` |
| GET | `/{apiVersion}/account/betas/{betaId}` |
| POST | `/{apiVersion}/account/cancel` |
| GET | `/{apiVersion}/account/child-accounts` |
| GET | `/{apiVersion}/account/child-accounts/{euuId}` |
| POST | `/{apiVersion}/account/child-accounts/{euuId}/token` |
| POST | `/{apiVersion}/account/credit-card` |
| POST,GET | `/{apiVersion}/account/entity-transfers` |
| GET,DELETE | `/{apiVersion}/account/entity-transfers/{token}` |
| POST | `/{apiVersion}/account/entity-transfers/{token}/accept` |
| GET | `/{apiVersion}/account/events` |
| GET | `/{apiVersion}/account/events/{eventId}` |
| POST | `/{apiVersion}/account/events/{eventId}/seen` |
| GET | `/{apiVersion}/account/invoices` |
| GET | `/{apiVersion}/account/invoices/{invoiceId}` |
| GET | `/{apiVersion}/account/invoices/{invoiceId}/items` |
| GET | `/{apiVersion}/account/logins` |
| GET | `/{apiVersion}/account/logins/{loginId}` |
| GET | `/{apiVersion}/account/maintenance` |
| GET | `/{apiVersion}/account/notifications` |
| POST,GET | `/{apiVersion}/account/oauth-clients` |
| GET,PUT,DELETE | `/{apiVersion}/account/oauth-clients/{clientId}` |
| POST | `/{apiVersion}/account/oauth-clients/{clientId}/reset-secret` |
| GET,PUT | `/{apiVersion}/account/oauth-clients/{clientId}/thumbnail` |
| POST,GET | `/{apiVersion}/account/payment-methods` |
| GET,DELETE | `/{apiVersion}/account/payment-methods/{paymentMethodId}` |
| POST | `/{apiVersion}/account/payment-methods/{paymentMethodId}/make-default` |
| POST,GET | `/{apiVersion}/account/payments` |
| POST | `/{apiVersion}/account/payments/paypal` |
| POST | `/{apiVersion}/account/payments/paypal/execute` |
| GET | `/{apiVersion}/account/payments/{paymentId}` |
| POST | `/{apiVersion}/account/promo-codes` |
| POST,GET | `/{apiVersion}/account/service-transfers` |
| GET,DELETE | `/{apiVersion}/account/service-transfers/{token}` |
| POST | `/{apiVersion}/account/service-transfers/{token}/accept` |
| GET,PUT | `/{apiVersion}/account/settings` |
| POST | `/{apiVersion}/account/settings/managed-enable` |
| GET | `/{apiVersion}/account/transfer` |
| POST,GET | `/{apiVersion}/account/users` |
| GET,PUT,DELETE | `/{apiVersion}/account/users/{username}` |
| GET,PUT | `/{apiVersion}/account/users/{username}/grants` |
| GET | `/{apiVersion}/betas` |
| GET | `/{apiVersion}/betas/{betaId}` |
| GET | `/{apiVersion}/databases/engines` |
| GET | `/{apiVersion}/databases/engines/{engineId}` |
| GET | `/{apiVersion}/databases/instances` |
| GET | `/{apiVersion}/databases/mysql/config` |
| POST,GET | `/{apiVersion}/databases/mysql/instances` |
| GET,PUT,DELETE | `/{apiVersion}/databases/mysql/instances/{instanceId}` |
| GET | `/{apiVersion}/databases/mysql/instances/{instanceId}/credentials` |
| POST | `/{apiVersion}/databases/mysql/instances/{instanceId}/credentials/reset` |
| POST | `/{apiVersion}/databases/mysql/instances/{instanceId}/patch` |
| POST | `/{apiVersion}/databases/mysql/instances/{instanceId}/resume` |
| GET | `/{apiVersion}/databases/mysql/instances/{instanceId}/ssl` |
| POST | `/{apiVersion}/databases/mysql/instances/{instanceId}/suspend` |
| GET | `/{apiVersion}/databases/postgresql/config` |
| POST,GET | `/{apiVersion}/databases/postgresql/instances` |
| GET,PUT,DELETE | `/{apiVersion}/databases/postgresql/instances/{instanceId}` |
| GET | `/{apiVersion}/databases/postgresql/instances/{instanceId}/credentials` |
| POST | `/{apiVersion}/databases/postgresql/instances/{instanceId}/credentials/reset` |
| POST | `/{apiVersion}/databases/postgresql/instances/{instanceId}/patch` |
| POST | `/{apiVersion}/databases/postgresql/instances/{instanceId}/resume` |
| GET | `/{apiVersion}/databases/postgresql/instances/{instanceId}/ssl` |
| POST | `/{apiVersion}/databases/postgresql/instances/{instanceId}/suspend` |
| GET | `/{apiVersion}/databases/types` |
| GET | `/{apiVersion}/databases/types/{typeId}` |
| POST,GET | `/{apiVersion}/domains` |
| POST | `/{apiVersion}/domains/import` |
| GET,PUT,DELETE | `/{apiVersion}/domains/{domainId}` |
| POST | `/{apiVersion}/domains/{domainId}/clone` |
| POST,GET | `/{apiVersion}/domains/{domainId}/records` |
| GET,PUT,DELETE | `/{apiVersion}/domains/{domainId}/records/{recordId}` |
| GET | `/{apiVersion}/domains/{domainId}/zone-file` |
| POST,GET | `/{apiVersion}/images` |
| POST,GET | `/{apiVersion}/images/sharegroups` |
| POST,GET | `/{apiVersion}/images/sharegroups/tokens` |
| GET,PUT,DELETE | `/{apiVersion}/images/sharegroups/tokens/{tokenUuid}` |
| GET | `/{apiVersion}/images/sharegroups/tokens/{tokenUuid}/sharegroup` |
| GET | `/{apiVersion}/images/sharegroups/tokens/{tokenUuid}/sharegroup/images` |
| GET,PUT,DELETE | `/{apiVersion}/images/sharegroups/{sharegroupId}` |
| POST,GET | `/{apiVersion}/images/sharegroups/{sharegroupId}/images` |
| PUT,DELETE | `/{apiVersion}/images/sharegroups/{sharegroupId}/images/{imageId}` |
| POST,GET | `/{apiVersion}/images/sharegroups/{sharegroupId}/members` |
| GET,PUT,DELETE | `/{apiVersion}/images/sharegroups/{sharegroupId}/members/{tokenUuid}` |
| POST | `/{apiVersion}/images/upload` |
| GET,PUT,DELETE | `/{apiVersion}/images/{imageId}` |
| POST | `/{apiVersion}/images/{imageId}/regions` |
| GET | `/{apiVersion}/images/{imageId}/sharegroups` |
| POST,GET | `/{apiVersion}/linode/instances` |
| GET,PUT,DELETE | `/{apiVersion}/linode/instances/{linodeId}` |
| POST,GET | `/{apiVersion}/linode/instances/{linodeId}/backups` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/backups/cancel` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/backups/enable` |
| GET | `/{apiVersion}/linode/instances/{linodeId}/backups/{backupId}` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/backups/{backupId}/restore` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/boot` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/clone` |
| POST,GET | `/{apiVersion}/linode/instances/{linodeId}/configs` |
| GET,PUT,DELETE | `/{apiVersion}/linode/instances/{linodeId}/configs/{configId}` |
| POST,GET | `/{apiVersion}/linode/instances/{linodeId}/configs/{configId}/interfaces` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/configs/{configId}/interfaces/order` |
| GET,PUT,DELETE | `/{apiVersion}/linode/instances/{linodeId}/configs/{configId}/interfaces/{interfaceId}` |
| POST,GET | `/{apiVersion}/linode/instances/{linodeId}/disks` |
| GET,PUT,DELETE | `/{apiVersion}/linode/instances/{linodeId}/disks/{diskId}` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/disks/{diskId}/clone` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/disks/{diskId}/password` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/disks/{diskId}/resize` |
| GET,PUT | `/{apiVersion}/linode/instances/{linodeId}/firewalls` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/firewalls/apply` |
| POST,GET | `/{apiVersion}/linode/instances/{linodeId}/interfaces` |
| GET | `/{apiVersion}/linode/instances/{linodeId}/interfaces/history` |
| GET,PUT | `/{apiVersion}/linode/instances/{linodeId}/interfaces/settings` |
| GET,PUT,DELETE | `/{apiVersion}/linode/instances/{linodeId}/interfaces/{interfaceId}` |
| GET | `/{apiVersion}/linode/instances/{linodeId}/interfaces/{interfaceId}/firewalls` |
| POST,GET | `/{apiVersion}/linode/instances/{linodeId}/ips` |
| GET,PUT,DELETE | `/{apiVersion}/linode/instances/{linodeId}/ips/{address}` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/migrate` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/mutate` |
| GET | `/{apiVersion}/linode/instances/{linodeId}/nodebalancers` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/password` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/reboot` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/rebuild` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/rescue` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/resize` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/shutdown` |
| GET | `/{apiVersion}/linode/instances/{linodeId}/stats` |
| GET | `/{apiVersion}/linode/instances/{linodeId}/stats/{year}/{month}` |
| GET | `/{apiVersion}/linode/instances/{linodeId}/transfer` |
| GET | `/{apiVersion}/linode/instances/{linodeId}/transfer/{year}/{month}` |
| POST | `/{apiVersion}/linode/instances/{linodeId}/upgrade-interfaces` |
| GET | `/{apiVersion}/linode/instances/{linodeId}/volumes` |
| GET | `/{apiVersion}/linode/kernels` |
| GET | `/{apiVersion}/linode/kernels/{kernelId}` |
|  | `/{apiVersion}/linode/quotas` |
|  | `/{apiVersion}/linode/quotas/{linode-quotaId}` |
|  | `/{apiVersion}/linode/quotas/{linode-quotaId}/usage` |
| POST,GET | `/{apiVersion}/linode/stackscripts` |
| GET,PUT,DELETE | `/{apiVersion}/linode/stackscripts/{stackscriptId}` |
| GET | `/{apiVersion}/linode/types` |
| GET | `/{apiVersion}/linode/types/{typeId}` |
| POST,GET | `/{apiVersion}/lke/clusters` |
| GET,PUT,DELETE | `/{apiVersion}/lke/clusters/{clusterId}` |
| GET | `/{apiVersion}/lke/clusters/{clusterId}/api-endpoints` |
| GET,PUT,DELETE | `/{apiVersion}/lke/clusters/{clusterId}/control_plane_acl` |
| GET | `/{apiVersion}/lke/clusters/{clusterId}/dashboard` |
| GET,DELETE | `/{apiVersion}/lke/clusters/{clusterId}/kubeconfig` |
| GET,DELETE | `/{apiVersion}/lke/clusters/{clusterId}/nodes/{nodeId}` |
| POST | `/{apiVersion}/lke/clusters/{clusterId}/nodes/{nodeId}/recycle` |
| POST,GET | `/{apiVersion}/lke/clusters/{clusterId}/pools` |
| GET,PUT,DELETE | `/{apiVersion}/lke/clusters/{clusterId}/pools/{poolId}` |
| POST | `/{apiVersion}/lke/clusters/{clusterId}/pools/{poolId}/recycle` |
| POST | `/{apiVersion}/lke/clusters/{clusterId}/recycle` |
| POST | `/{apiVersion}/lke/clusters/{clusterId}/regenerate` |
| DELETE | `/{apiVersion}/lke/clusters/{clusterId}/servicetoken` |
|  | `/{apiVersion}/lke/quotas` |
|  | `/{apiVersion}/lke/quotas/{lke-quotaId}` |
|  | `/{apiVersion}/lke/quotas/{lke-quotaId}/usage` |
| GET | `/{apiVersion}/lke/tiers/{tier}/versions` |
| GET | `/{apiVersion}/lke/tiers/{tier}/versions/{version}` |
| GET | `/{apiVersion}/lke/types` |
| GET | `/{apiVersion}/lke/versions` |
| GET | `/{apiVersion}/lke/versions/{version}` |
| POST,GET | `/{apiVersion}/longview/clients` |
| GET,PUT,DELETE | `/{apiVersion}/longview/clients/{clientId}` |
| GET,PUT | `/{apiVersion}/longview/plan` |
| GET | `/{apiVersion}/longview/subscriptions` |
| GET | `/{apiVersion}/longview/subscriptions/{subscriptionId}` |
| GET | `/{apiVersion}/longview/types` |
| GET | `/{apiVersion}/maintenance/policies` |
| POST,GET | `/{apiVersion}/managed/contacts` |
| GET,PUT,DELETE | `/{apiVersion}/managed/contacts/{contactId}` |
| POST,GET | `/{apiVersion}/managed/credentials` |
| GET | `/{apiVersion}/managed/credentials/sshkey` |
| GET,PUT | `/{apiVersion}/managed/credentials/{credentialId}` |
| POST | `/{apiVersion}/managed/credentials/{credentialId}/revoke` |
| POST | `/{apiVersion}/managed/credentials/{credentialId}/update` |
| GET | `/{apiVersion}/managed/issues` |
| GET | `/{apiVersion}/managed/issues/{issueId}` |
| GET | `/{apiVersion}/managed/linode-settings` |
| GET,PUT | `/{apiVersion}/managed/linode-settings/{linodeId}` |
| POST,GET | `/{apiVersion}/managed/services` |
| GET,PUT,DELETE | `/{apiVersion}/managed/services/{serviceId}` |
| POST | `/{apiVersion}/managed/services/{serviceId}/disable` |
| POST | `/{apiVersion}/managed/services/{serviceId}/enable` |
| GET | `/{apiVersion}/managed/stats` |
| GET | `/{apiVersion}/monitor/alert-channels` |
| GET | `/{apiVersion}/monitor/alert-definitions` |
| GET | `/{apiVersion}/monitor/dashboards` |
| GET | `/{apiVersion}/monitor/dashboards/{dashboardId}` |
| GET | `/{apiVersion}/monitor/services` |
| GET | `/{apiVersion}/monitor/services/{serviceType}` |
| POST,GET | `/{apiVersion}/monitor/services/{serviceType}/alert-definitions` |
| GET,PUT,DELETE | `/{apiVersion}/monitor/services/{serviceType}/alert-definitions/{alertId}` |
| GET | `/{apiVersion}/monitor/services/{serviceType}/dashboards` |
| GET | `/{apiVersion}/monitor/services/{serviceType}/metric-definitions` |
| POST | `/{apiVersion}/monitor/services/{serviceType}/metrics` |
| POST | `/{apiVersion}/monitor/services/{serviceType}/token` |
|  | `/{apiVersion}/monitor/streams` |
|  | `/{apiVersion}/monitor/streams/destinations` |
|  | `/{apiVersion}/monitor/streams/destinations/{destinationId}` |
|  | `/{apiVersion}/monitor/streams/destinations/{destinationId}/history` |
|  | `/{apiVersion}/monitor/streams/{streamId}` |
|  | `/{apiVersion}/monitor/streams/{streamId}/history` |
|  | `/{apiVersion}/monitor/streams/{streamId}/stats` |
| GET | `/{apiVersion}/network-transfer/prices` |
| POST,GET | `/{apiVersion}/networking/firewalls` |
| GET,PUT | `/{apiVersion}/networking/firewalls/settings` |
| GET | `/{apiVersion}/networking/firewalls/templates` |
| GET | `/{apiVersion}/networking/firewalls/templates/{slug}` |
| GET,PUT,DELETE | `/{apiVersion}/networking/firewalls/{firewallId}` |
| POST,GET | `/{apiVersion}/networking/firewalls/{firewallId}/devices` |
| GET,DELETE | `/{apiVersion}/networking/firewalls/{firewallId}/devices/{deviceId}` |
| GET | `/{apiVersion}/networking/firewalls/{firewallId}/history` |
| GET | `/{apiVersion}/networking/firewalls/{firewallId}/history/rules/{version}` |
| GET,PUT | `/{apiVersion}/networking/firewalls/{firewallId}/rules` |
| POST,GET | `/{apiVersion}/networking/ips` |
| POST | `/{apiVersion}/networking/ips/assign` |
| POST | `/{apiVersion}/networking/ips/share` |
| GET,PUT | `/{apiVersion}/networking/ips/{address}` |
| POST | `/{apiVersion}/networking/ipv4/assign` |
| POST | `/{apiVersion}/networking/ipv4/share` |
| GET | `/{apiVersion}/networking/ipv6/pools` |
| POST,GET | `/{apiVersion}/networking/ipv6/ranges` |
| GET,DELETE | `/{apiVersion}/networking/ipv6/ranges/{range}` |
| GET | `/{apiVersion}/networking/vlans` |
| DELETE | `/{apiVersion}/networking/vlans/{regionId}/{label}` |
| POST,GET | `/{apiVersion}/nodebalancers` |
| GET | `/{apiVersion}/nodebalancers/types` |
| GET,PUT,DELETE | `/{apiVersion}/nodebalancers/{nodeBalancerId}` |
| POST,GET | `/{apiVersion}/nodebalancers/{nodeBalancerId}/configs` |
| GET,PUT,DELETE | `/{apiVersion}/nodebalancers/{nodeBalancerId}/configs/{configId}` |
| POST,GET | `/{apiVersion}/nodebalancers/{nodeBalancerId}/configs/{configId}/nodes` |
| GET,PUT,DELETE | `/{apiVersion}/nodebalancers/{nodeBalancerId}/configs/{configId}/nodes/{nodeId}` |
| POST | `/{apiVersion}/nodebalancers/{nodeBalancerId}/configs/{configId}/rebuild` |
| GET,PUT | `/{apiVersion}/nodebalancers/{nodeBalancerId}/firewalls` |
| GET | `/{apiVersion}/nodebalancers/{nodeBalancerId}/stats` |
| GET | `/{apiVersion}/nodebalancers/{nodeBalancerId}/vpcs` |
| GET | `/{apiVersion}/nodebalancers/{nodeBalancerId}/vpcs/{nodeBalancerVpcConfigId}` |
| POST,GET | `/{apiVersion}/object-storage/buckets` |
| GET | `/{apiVersion}/object-storage/buckets/{regionId}` |
| GET,DELETE | `/{apiVersion}/object-storage/buckets/{regionId}/{bucket}` |
| POST,GET,PUT | `/{apiVersion}/object-storage/buckets/{regionId}/{bucket}/access` |
| GET,PUT | `/{apiVersion}/object-storage/buckets/{regionId}/{bucket}/object-acl` |
| GET | `/{apiVersion}/object-storage/buckets/{regionId}/{bucket}/object-list` |
| POST | `/{apiVersion}/object-storage/buckets/{regionId}/{bucket}/object-url` |
| POST,GET,DELETE | `/{apiVersion}/object-storage/buckets/{regionId}/{bucket}/ssl` |
| POST | `/{apiVersion}/object-storage/cancel` |
| GET | `/{apiVersion}/object-storage/clusters` |
| GET | `/{apiVersion}/object-storage/clusters/{clusterId}` |
| GET | `/{apiVersion}/object-storage/endpoints` |
| POST,GET | `/{apiVersion}/object-storage/keys` |
| GET,PUT,DELETE | `/{apiVersion}/object-storage/keys/{keyId}` |
| GET | `/{apiVersion}/object-storage/quotas` |
| GET | `/{apiVersion}/object-storage/quotas/{objQuotaId}` |
| GET | `/{apiVersion}/object-storage/quotas/{objQuotaId}/usage` |
| GET | `/{apiVersion}/object-storage/transfer` |
| GET | `/{apiVersion}/object-storage/types` |
| POST,GET | `/{apiVersion}/placement/groups` |
| GET,PUT,DELETE | `/{apiVersion}/placement/groups/{groupId}` |
| POST | `/{apiVersion}/placement/groups/{groupId}/assign` |
| POST | `/{apiVersion}/placement/groups/{groupId}/unassign` |
| GET,PUT | `/{apiVersion}/profile` |
| GET | `/{apiVersion}/profile/apps` |
| GET,DELETE | `/{apiVersion}/profile/apps/{appId}` |
| GET | `/{apiVersion}/profile/devices` |
| GET,DELETE | `/{apiVersion}/profile/devices/{deviceId}` |
| GET | `/{apiVersion}/profile/grants` |
| GET | `/{apiVersion}/profile/logins` |
| GET | `/{apiVersion}/profile/logins/{loginId}` |
| POST,DELETE | `/{apiVersion}/profile/phone-number` |
| POST | `/{apiVersion}/profile/phone-number/verify` |
| GET,PUT | `/{apiVersion}/profile/preferences` |
| POST,GET | `/{apiVersion}/profile/security-questions` |
| POST,GET | `/{apiVersion}/profile/sshkeys` |
| GET,PUT,DELETE | `/{apiVersion}/profile/sshkeys/{sshKeyId}` |
| POST | `/{apiVersion}/profile/tfa-disable` |
| POST | `/{apiVersion}/profile/tfa-enable` |
| POST | `/{apiVersion}/profile/tfa-enable-confirm` |
| POST,GET | `/{apiVersion}/profile/tokens` |
| GET,PUT,DELETE | `/{apiVersion}/profile/tokens/{tokenId}` |
| GET | `/{apiVersion}/regions` |
| GET | `/{apiVersion}/regions/availability` |
| GET | `/{apiVersion}/regions/{regionId}` |
| GET | `/{apiVersion}/regions/{regionId}/availability` |
| POST,GET | `/{apiVersion}/support/tickets` |
| GET | `/{apiVersion}/support/tickets/{ticketId}` |
| POST | `/{apiVersion}/support/tickets/{ticketId}/attachments` |
| POST | `/{apiVersion}/support/tickets/{ticketId}/close` |
| POST,GET | `/{apiVersion}/support/tickets/{ticketId}/replies` |
| POST,GET | `/{apiVersion}/tags` |
| GET,DELETE | `/{apiVersion}/tags/{tagLabel}` |
| POST,GET | `/{apiVersion}/volumes` |
| GET | `/{apiVersion}/volumes/types` |
| GET,PUT,DELETE | `/{apiVersion}/volumes/{volumeId}` |
| POST | `/{apiVersion}/volumes/{volumeId}/attach` |
| POST | `/{apiVersion}/volumes/{volumeId}/clone` |
| POST | `/{apiVersion}/volumes/{volumeId}/detach` |
| POST | `/{apiVersion}/volumes/{volumeId}/resize` |
| POST,GET | `/{apiVersion}/vpcs` |
| GET | `/{apiVersion}/vpcs/ips` |
| GET,PUT,DELETE | `/{apiVersion}/vpcs/{vpcId}` |
| GET | `/{apiVersion}/vpcs/{vpcId}/ips` |
| POST,GET | `/{apiVersion}/vpcs/{vpcId}/subnets` |
| GET,PUT,DELETE | `/{apiVersion}/vpcs/{vpcId}/subnets/{vpcSubnetId}` |

</details>

## Nebius dedicated endpoint templates (public GET /v0/dedicated_endpoints/templates)

Templates: 43. Types: text2text (33), image2text (6), embedding (4)

Flavor quantization: fp8 (33), fp16 (8), fp4 (4), int4 (2), bf16 (1)

GPU type by region (flavor count): gpu-h100-sxm in eu-north1 (20), gpu-h200-sxm in us-central1 (41), gpu-l40s-d in eu-north1 (6)

| Model | Flavor | Quantization | GPU types at regions | Max replicas | Context (K) |
| --- | --- | --- | --- | --- | --- |
| BAAI/bge-en-icl | base | fp16 | gpu-l40s-d@eu-north1 | 32 | 32 |
| BAAI/bge-multilingual-gemma2 | base | fp16 | gpu-l40s-d@eu-north1 | 32 | 8 |
| MiniMaxAI/MiniMax-M2.1 | base | fp8 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 196 |
| NousResearch/Hermes-4-405B | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 128 |
| NousResearch/Hermes-4-70B | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 128 |
| PrimeIntellect/INTELLECT-3 | base | fp8 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 128 |
| Qwen/Qwen2.5-Coder-7B-fast | fast | fp8 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 32 |
| Qwen/Qwen2.5-VL-72B-Instruct | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 32 |
| Qwen/Qwen3-235B-A22B-Instruct-2507 | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 262 |
| Qwen/Qwen3-235B-A22B-Thinking-2507 | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 262 |
| Qwen/Qwen3-30B-A3B-Instruct-2507 | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 262 |
| Qwen/Qwen3-30B-A3B-Thinking-2507 | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 262 |
| Qwen/Qwen3-32B | base | fp8 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 41 |
| Qwen/Qwen3-32B | fast | fp8 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 41 |
| Qwen/Qwen3-Coder-30B-A3B-Instruct | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 262 |
| Qwen/Qwen3-Coder-480B-A35B-Instruct | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 262 |
| Qwen/Qwen3-Embedding-8B | base | fp16 | gpu-l40s-d@eu-north1 | 32 | 41 |
| Qwen/Qwen3-Next-80B-A3B-Thinking | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 128 |
| deepseek-ai/DeepSeek-R1-0528 | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 32 |
| deepseek-ai/DeepSeek-V3-0324 | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 32 |
| google/gemma-2-2b-it | base | fp16 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 8 |
| google/gemma-2-9b-it-fast | fast | fp8 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 8 |
| google/gemma-3-27b-it | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 110 |
| google/gemma-3-27b-it | fast | fp8 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 110 |
| intfloat/e5-mistral-7b-instruct | base | fp16 | gpu-l40s-d@eu-north1 | 32 | 32 |
| meta-llama/Llama-3.3-70B-Instruct | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 128 |
| meta-llama/Llama-3.3-70B-Instruct | fast | fp8 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 128 |
| meta-llama/Llama-Guard-3-8B | base | fp16 | gpu-l40s-d@eu-north1 | 32 | 128 |
| meta-llama/Meta-Llama-3.1-8B-Instruct-fast | base | fp8 | gpu-l40s-d@eu-north1 | 32 | 128 |
| meta-llama/Meta-Llama-3.1-8B-Instruct-fast | fast | fp8 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 128 |
| moonshotai/Kimi-K2-Instruct | base | fp4 | gpu-h200-sxm@us-central1 | 32 | 131 |
| moonshotai/Kimi-K2-Thinking | base | int4 | gpu-h200-sxm@us-central1 | 32 | 262 |
| moonshotai/Kimi-K2.5 | base | int4 | gpu-h200-sxm@us-central1 | 8 | 256 |
| nvidia/Cosmos3-Super-Reasoner | base | fp16 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 256 |
| nvidia/Llama-3_1-Nemotron-Ultra-253B-v1 | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 128 |
| nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B | base | fp8 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 262 |
| nvidia/Nemotron-3-Nano-Omni | base | fp8 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 262 |
| nvidia/Nemotron-Nano-V2-12b | base | bf16 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 128 |
| openai/gpt-oss-120b | base | fp4 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 131 |
| openai/gpt-oss-120b | fast | fp4 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 8 | 131 |
| openai/gpt-oss-20b | base | fp4 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 131 |
| openbmb/MiniCPM-V-4_5 | base | fp16 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 32 |
| qwen/qwen3-vl-32b | base | fp8 | gpu-h100-sxm@eu-north1 | 8 | 256 |
| zai-org/GLM-4.5 | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 128 |
| zai-org/GLM-4.5-Air | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 128 |
| zai-org/GLM-4.7-FP8 | base | fp8 | gpu-h100-sxm@eu-north1, gpu-h200-sxm@us-central1 | 32 | 200 |
| zai-org/GLM-5.1 | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 200 |
| zai-org/GLM-5.2 | base | fp8 | gpu-h200-sxm@us-central1 | 32 | 432 |

