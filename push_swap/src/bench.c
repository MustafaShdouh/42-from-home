/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bench.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/14 00:17:19 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/14 01:10:23 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"
#include "libft.h"

t_op_stats	*get_stats(void)
{
	static t_op_stats	stats;

	return (&stats);
}

int	get_total_ops(void)
{
	t_op_stats	*s;

	s = get_stats();
	return (s->sa + s->sb + s->ss + s->pa + s->pb
		+ s->ra + s->rb + s->rr + s->rra + s->rrb
		+ s->rrr);
}

static void	print_ops_row1(t_op_stats *s)
{
	ft_putstr_fd("[bench] sa: ", 2);
	ft_putnbr_fd(s->sa, 2);
	ft_putstr_fd(" sb: ", 2);
	ft_putnbr_fd(s->sb, 2);
	ft_putstr_fd(" ss: ", 2);
	ft_putnbr_fd(s->ss, 2);
	ft_putstr_fd(" pa: ", 2);
	ft_putnbr_fd(s->pa, 2);
	ft_putstr_fd(" pb: ", 2);
	ft_putnbr_fd(s->pb, 2);
	ft_putstr_fd("\n", 2);
}

static void	print_ops_row2(t_op_stats *s)
{
	ft_putstr_fd("[bench] ra: ", 2);
	ft_putnbr_fd(s->ra, 2);
	ft_putstr_fd(" rb: ", 2);
	ft_putnbr_fd(s->rb, 2);
	ft_putstr_fd(" rr: ", 2);
	ft_putnbr_fd(s->rr, 2);
	ft_putstr_fd(" rra: ", 2);
	ft_putnbr_fd(s->rra, 2);
	ft_putstr_fd(" rrb: ", 2);
	ft_putnbr_fd(s->rrb, 2);
	ft_putstr_fd(" rrr: ", 2);
	ft_putnbr_fd(s->rrr, 2);
	ft_putstr_fd("\n", 2);
}

void	print_bench(t_strategy mode, double disorder)
{
	ft_putstr_fd("[bench] disorder: ", 2);
	ft_putfloat_fd(disorder * 100, 2);
	ft_putstr_fd("%\n[bench] strategy: ", 2);
	if (mode == START_SIMPLE)
		ft_putstr_fd("Simple (Min-Max) / O(n^2)\n", 2);
	else if (mode == START_MEDIUM)
		ft_putstr_fd("Medium (Chunk Sort) / O(n * sqrt(n)\n", 2);
	else if (mode == START_COMPLEX)
		ft_putstr_fd("Complex (Radix) / O(n log n)\n", 2);
	else if (mode == START_ADAPTIVE)
	{
		if (disorder <= 0.2)
			ft_putstr_fd("Adaptive / O(n^2)\n", 2);
		else if (disorder <= 0.5)
			ft_putstr_fd("Adaptive / O(n * sqrt(n))\n", 2);
		else
			ft_putstr_fd("Adaptive / O(n * log(n))\n", 2);
	}
	ft_putstr_fd("[bench] total_ops: ", 2);
	ft_putnbr_fd(get_total_ops(), 2);
	ft_putstr_fd("\n", 2);
	print_ops_row1(get_stats());
	print_ops_row2(get_stats());
}
