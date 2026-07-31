// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'introduction',
      label: 'Overview',
    },
    {
      type: 'category',
      label: 'Quickstart',
      items: [
        { type: 'doc', id: 'ita/Quickstart/howto-manage-subscriptions', label: 'Subscriptions' },
        { type: 'doc', id: 'ita/Quickstart/tutorial-api-key', label: 'Getting Started' },
      ],
    },
    {
      type: 'category',
      label: 'Tutorials and examples',
      items: [
        { type: 'doc', id: 'ita/Tutorials and examples/tutorial-cicd', label: 'CI/CD Integration' },
        { type: 'doc', id: 'ita/Tutorials and examples/tutorial-tdx-workload', label: 'TDX AI model key release demo' },
        {
          type: 'category',
          label: 'Trust Authority Client Examples',
          items: [
            { type: 'doc', id: 'ita/Tutorials and examples/Intel Trust Authority Client examples/tutorial-tdx', label: 'Client examples for TDX on Microsoft Azure*' },
            { type: 'doc', id: 'ita/Tutorials and examples/Intel Trust Authority Client examples/tutorial-tdx-gcp', label: 'Client examples for TDX on GCP*' },
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'How-to workflows',
      items: [
        { type: 'doc', id: 'ita/How-to workflows/howto-manage-users', label: 'User management' },
        { type: 'doc', id: 'ita/How-to workflows/howto-manage-attestation-policies', label: 'Policies' },
        { type: 'doc', id: 'ita/How-to workflows/howto-SIEM-integration', label: 'SIEM integration' },
      ],
    },
    {
      type: 'category',
      label: 'Attestation technologies',
      items: [
        {
          type: 'category',
          label: 'Trusted execution environments',
          link: { type: 'doc', id: 'ita/Attestation Technologies/concept-tees-overview' },
          items: [
            { type: 'doc', id: 'ita/Attestation Technologies/Trusted execution environments/tee-sgx', label: 'SGX' },
            { type: 'doc', id: 'ita/Attestation Technologies/Trusted execution environments/integrate-tdx-adapter-api', label: ' TDX' },
            { type: 'doc', id: 'ita/Attestation Technologies/Trusted execution environments/tee-sev-snp', label: 'AMD SEV-SNP' },
          ],
        },
        { type: 'doc', id: 'ita/Attestation Technologies/GPU confidential computing/concept-gpu-attestation', label: 'GPU confidential computing' },
      ],
    },
    {
      type: 'category',
      label: 'Concepts',
      items: [
        { type: 'doc', id: 'ita/Concepts/concept-attestation-overview', label: 'Attestation overview' },
        { type: 'doc', id: 'ita/Concepts/concept-patterns', label: 'Attestation patterns' },
        { type: 'doc', id: 'ita/Concepts/concept-policy-v2', label: 'Attestation policy V2' },
      ],
    },
    {
      type: 'category',
      label: 'Resources',
      items: [
        {
          type: 'category',
          label: 'Tenant Administration CLI',
          link: { type: 'doc', id: 'ita/Command-line/cli-examples' },
          items: [
            { type: 'doc', id: 'ita/Command-line/cli-install', label: 'Installation' },
            { type: 'doc', id: 'ita/Command-line/cli-policy-commands', label: 'Policy management' },
            { type: 'doc', id: 'ita/Command-line/cli-api-client-management', label: 'API client management' },
          ],
        },
        {
          type: 'category',
          label: 'Key Broker Service',
          link: { type: 'doc', id: 'ita/Key-broker/key-broker-service' },
          items: [
            { type: 'doc', id: 'ita/Key-broker/key-broker-service-kms-install', label: 'Key Management Service installation' },
            { type: 'doc', id: 'ita/Key-broker/key-broker-service-install', label: 'KBS installation' },
            { type: 'doc', id: 'ita/Key-broker/kbs.key.creation.retrieval', label: 'Key creation and retrieval' },
          ],
        },
      ],
    },
  ],
};

export default sidebars;