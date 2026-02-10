/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_complex.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/06 20:53:30 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/10 20:46:18 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	get_max_bits(t_stack **stack)
{
	t_stack	*head;
	int	max;
	int	max_bits;

	head = *stack;
	max = head->index;
	max_bits = 0;
	while (head)
	{
		if (head->index > max)
			max = head->index;
		head = head->next;
	}
	while ((max >> max_bits) != 0)
		max_bits++;
	return (max_bits);
}

static void radix_sort(t_stack **a, t_stack **b, int size)
{
	t_stack	*head_a;
	int	i;
	int	j;
	int	max_bits;

	max_bits = get_max_bits(a);
	i = 0;
	while (i < max_bits)
	{
		j = 0;
		while (j < size)
		{
			head_a = *a;
			if (((head_a->index >> i) & 1) == 1)
				ra(a);
			else
				pb(a, b);
			j++;
 		}
		while (*b)
			pa(a, b);
		i++;
	}
}

void	sort_complex(t_stack **a, t_stack **b)
{
	int	size;

	size = ft_lstsize(*a);
	index_stack(a);
	radix_sort(a, b, size);
}
